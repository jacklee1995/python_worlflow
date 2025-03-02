from typing import List, Dict, Any
import pandas as pd

from workflow_engine.interfaces.step_interface import StepInterface
from workflow_engine.interfaces.source_interface import SourceInterface
from workflow_engine.interfaces.output_interface import OutputInterface
from workflow_engine.interfaces.config_interface import ConfigInterface


class PivotStep(StepInterface):
    """
    数据透视步骤。

    对数据进行透视操作,生成透视表。
    """

    def __init__(self, name: str = 'PivotStep', description: str = 'Pivot data'):
        """
        初始化PivotStep。

        Args:
            name (str): 步骤名称。
            description (str): 步骤描述。
        """
        self.name = name
        self.description = description
        self.config = None
        self.sources = []
        self.output = None
        self.index = None
        self.columns = None
        self.values = None
        self.aggfunc = 'mean'

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

    def set_index(self, index: List[str]) -> None:
        """
        设置透视表的索引列。

        Args:
            index (List[str]): 索引列。
        """
        self.index = index

    def set_columns(self, columns: List[str]) -> None:
        """
        设置透视表的列。

        Args:
            columns (List[str]): 列。
        """
        self.columns = columns

    def set_values(self, values: List[str]) -> None:
        """
        设置透视表的值。

        Args:
            values (List[str]): 值。
        """
        self.values = values

    def set_aggfunc(self, aggfunc: str) -> None:
        """
        设置聚合函数。

        Args:
            aggfunc (str): 聚合函数。
        """
        self.aggfunc = aggfunc

    async def execute(self) -> None:
        """
        执行透视步骤。

        对数据进行透视操作,生成透视表。
        """
        for source in self.sources:
            async for data in source.read_chunks():
                if isinstance(data, bytes):
                    df = pd.read_csv(pd.io.common.BytesIO(data))
                    pivot_table = pd.pivot_table(
                        df,
                        index=self.index,
                        columns=self.columns,
                        values=self.values,
                        aggfunc=self.aggfunc
                    )
                    output_buffer = pd.io.common.StringIO()
                    pivot_table.to_csv(output_buffer)
                    await self.output.write(output_buffer.getvalue().encode())

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