from typing import List, Callable, AsyncIterator, Optional
from workflow_engine.interfaces.step_interface import StepInterface
from workflow_engine.interfaces.source_interface import SourceInterface
from workflow_engine.interfaces.output_interface import OutputInterface
from workflow_engine.interfaces.config_interface import ConfigInterface


class TransformStep(StepInterface):
    """
    数据转换步骤。

    对数据进行转换操作。
    """

    def __init__(self, transformer: Callable, name: str = 'TransformStep', description: str = 'Transform data'):
        """
        初始化TransformStep。

        Args:
            transformer (Callable): 数据转换函数。
            name (str): 步骤名称。
            description (str): 步骤描述。
        """
        self.name = name
        self.description = description
        self.config = None
        self.sources = []
        self.output = None
        self.transformer = transformer

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

    def set_transformer(self, transformer: Callable) -> None:
        """
        设置数据转换函数。

        Args:
            transformer (Callable): 数据转换函数。
        """
        self.transformer = transformer

    async def execute(self) -> None:
        """
        执行数据转换步骤。

        对数据进行转换操作。
        """
        for source in self.sources:
            async for data in source.read_chunks():
                transformed_data = self.transformer(data)
                await self.output.write(transformed_data)

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
        await source.open()  # 打开数据源
        
        async for data in source.read_chunks():
            transformed_data = self.transformer(data)
            yield transformed_data

        await source.close()  # 关闭数据源

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
        pass

    def off(self, event: str, callback: Optional[Callable] = None) -> None:
        """
        移除事件处理器
        
        Args:
            event: 事件名称
            callback: 要移除的处理函数,为None则移除该事件所有处理器
        """
        pass 