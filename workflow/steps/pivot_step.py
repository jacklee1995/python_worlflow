from typing import List, Dict, Any
import pandas as pd

from workflow.interfaces.step_interface import StepInterface
from workflow.interfaces.source_interface import SourceInterface
from workflow.interfaces.destination_interface import DestinationInterface
from workflow.interfaces.config_interface import ConfigInterface


class PivotStep(StepInterface):
    """
    数据透视步骤。

    对数据进行透视操作，生成透视表。
    """

    def __init__(self, name: str = 'PivotStep', description: str = 'Pivot data'):
        """
        初始化 PivotStep。

        Args:
            name (str): 步骤名称。
            description (str): 步骤描述。
        """
        self.name = name
        self.description = description
        self.config = None
        self.sources = []
        self.destination = None
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

    def set_destination(self, destination: DestinationInterface) -> None:
        """
        设置步骤的输出目标。

        Args:
            destination (DestinationInterface): 步骤的输出目标。
        """
        self.destination = destination

    def get_destination(self) -> DestinationInterface:
        """
        获取步骤的输出目标。

        Returns:
            DestinationInterface: 步骤的输出目标。
        """
        return self.destination

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

    def execute(self) -> None:
        """
        执行透视步骤。

        对数据进行透视操作，生成透视表。
        """
        for source in self.sources:
            if source.is_file() and source.get_path().endswith('.csv'):
                df = pd.read_csv(source.get_path())
                pivot_table = pd.pivot_table(
                    df,
                    index=self.index,
                    columns=self.columns,
                    values=self.values,
                    aggfunc=self.aggfunc
                )
                pivot_table.to_csv(self.destination.get_path())

    def pipe(self, step: StepInterface) -> StepInterface:
        """
        将当前步骤的输出连接到另一个步骤的输入。

        Args:
            step (StepInterface): 下一个步骤。

        Returns:
            StepInterface: 下一个步骤。
        """
        step.set_sources([self.destination])
        return step 