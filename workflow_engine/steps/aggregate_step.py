from typing import List, Dict, Any, AsyncIterator, Optional, Callable
from workflow_engine.interfaces.step_interface import StepInterface
from workflow_engine.interfaces.source_interface import SourceInterface
from workflow_engine.interfaces.output_interface import OutputInterface
from workflow_engine.interfaces.config_interface import ConfigInterface
import json
import csv
from io import StringIO


class AggregateStep(StepInterface):
    """
    聚合步骤。

    对数据进行聚合操作,如求和、平均值等。
    """

    def __init__(self, name: str = 'AggregateStep', description: str = 'Aggregate data'):
        """
        初始化AggregateStep。

        Args:
            name (str): 步骤名称。
            description (str): 步骤描述。
        """
        self.name = name
        self.description = description
        self.config = None
        self.sources = []
        self.output = None
        self.aggregation_functions = {}
        self.aggregated_data = {}
        self._event_handlers = {
            'data': [],
            'error': [],
            'end': [],
            'close': [],
            'pipe': [],
            'unpipe': []
        }

    def get_name(self) -> str:
        """
        获取步骤名称。

        Returns:
            str: 步骤名称。
        """
        return self.name

    def set_name(self, name: str) -> None:
        """
        设置步骤名称。

        Args:
            name (str): 步骤名称。
        """
        self.name = name

    def get_description(self) -> str:
        """
        获取步骤描述。

        Returns:
            str: 步骤描述。
        """
        return self.description

    def set_description(self, description: str) -> None:
        """
        设置步骤描述。

        Args:
            description (str): 步骤描述。
        """
        self.description = description

    def set_config(self, config: ConfigInterface) -> None:
        """
        设置步骤的配置。

        Args:
            config (ConfigInterface): 步骤的配置。
        """
        self.config = config

    def get_config(self) -> ConfigInterface:
        """
        获取步骤的配置。

        Returns:
            ConfigInterface: 步骤的配置。
        """
        return self.config

    def set_sources(self, sources: List[SourceInterface]) -> None:
        """
        设置步骤的数据源。

        Args:
            sources (List[SourceInterface]): 步骤的数据源列表。
        """
        self.sources = sources

    def get_sources(self) -> List[SourceInterface]:
        """
        获取步骤的数据源。

        Returns:
            List[SourceInterface]: 步骤的数据源列表。
        """
        return self.sources

    def set_output(self, output: OutputInterface) -> None:
        """
        设置步骤的输出。

        Args:
            output (OutputInterface): 步骤的输出。
        """
        self.output = output

    def get_output(self) -> OutputInterface:
        """
        获取步骤的输出。

        Returns:
            OutputInterface: 步骤的输出。
        """
        return self.output

    def set_aggregation_functions(self, functions: Dict[str, Callable]) -> None:
        """
        设置聚合函数。

        Args:
            functions (Dict[str, Callable]): 聚合函数字典。
        """
        self.aggregation_functions = functions

    def get_aggregation_functions(self) -> Dict[str, Callable]:
        """
        获取聚合函数。

        Returns:
            Dict[str, Callable]: 聚合函数字典。
        """
        return self.aggregation_functions

    async def execute(self) -> AsyncIterator[bytes]:
        """
        执行聚合步骤。

        对数据进行聚合操作,如求和、平均值等。
        """
        if not self.sources:
            raise ValueError("No sources provided")

        try:
            for source in self.sources:
                await source.open()
                try:
                    async for data in source.read_chunks():
                        # 将字节串解码为 UTF-8 字符串
                        csv_data = data.decode('utf-8')
                        
                        # 使用 csv 模块解析 CSV 数据
                        reader = csv.DictReader(StringIO(csv_data))
                        for row in reader:
                            # 输出每行原始数据
                            if self.output:
                                await self.output.write(json.dumps({}).encode())
                                await self.output.write(json.dumps(row, indent=2).encode())
                            yield json.dumps(row).encode()
                            
                            # 累积数据进行聚合
                            for field in self.aggregation_functions.keys():
                                if field in row:
                                    try:
                                        value = float(row[field])
                                        if field not in self.aggregated_data:
                                            self.aggregated_data[field] = []
                                        self.aggregated_data[field].append(value)
                                    except (ValueError, TypeError):
                                        continue
                finally:
                    await source.close()

            # 输出聚合结果
            result = {}
            for field, values in self.aggregated_data.items():
                if values:
                    func = self.aggregation_functions.get(field)
                    if func:
                        if isinstance(func, str) and func == "mean":
                            result[field] = sum(values) / len(values)
                        else:
                            result[field] = func(values)

            if self.output:
                await self.output.write(json.dumps(result, indent=2).encode())
            yield json.dumps(result).encode()

        except Exception as e:
            for handler in self._event_handlers['error']:
                handler(e)
            raise

    async def pipe(self, step: StepInterface) -> StepInterface:
        """
        将当前步骤的输出连接到另一个步骤的输入。

        Args:
            step (StepInterface): 下一个步骤。

        Returns:
            StepInterface: 下一个步骤。
        """
        step.set_sources([self.output])
        return step

    async def process(self, source: SourceInterface) -> AsyncIterator[bytes]:
        """
        处理输入流并生成输出流
        
        Args:
            source: 输入数据流
            
        Returns:
            处理后的输出数据流
        """
        await source.open()
        
        aggregated_data = {}
        while True:
            data = await source.read()
            if not data:
                break
            if isinstance(data, dict):
                for field, func in self.aggregation_functions.items():
                    if field in data:
                        if field not in aggregated_data:
                            aggregated_data[field] = []
                        aggregated_data[field].append(data[field])

        result = {}
        for field, values in aggregated_data.items():
            func = self.aggregation_functions.get(field)
            if func:
                result[field] = func(values)

        await source.close()
        
        yield result

    async def transform(self, chunk: bytes) -> bytes:
        """
        转换数据块
        
        Args:
            chunk: 输入数据块
            
        Returns:
            转换后的数据块
        """
        return chunk

    def on(self, event: str, callback: Callable) -> None:
        """
        注册事件处理器
        
        Args:
            event: 事件名称
            callback: 事件处理函数
        """
        if event not in self._event_handlers:
            raise ValueError(f"Unsupported event: {event}")
        self._event_handlers[event].append(callback)

    def off(self, event: str, callback: Optional[Callable] = None) -> None:
        """
        移除事件处理器
        
        Args:
            event: 事件名称
            callback: 要移除的处理函数,为None则移除该事件所有处理器
        """
        if event not in self._event_handlers:
            raise ValueError(f"Unsupported event: {event}")
        if callback is None:
            self._event_handlers[event].clear()
        else:
            self._event_handlers[event] = [
                h for h in self._event_handlers[event] if h != callback
            ] 