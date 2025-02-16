from typing import List, Dict, Any
from workflow.interfaces.step_interface import StepInterface
from workflow.interfaces.source_interface import SourceInterface
from workflow.interfaces.destination_interface import DestinationInterface
from workflow.interfaces.config_interface import ConfigInterface


class AggregateStep(StepInterface):
    """
    聚合步骤。

    对数据进行聚合操作，如求和、平均值等。
    """

    def __init__(self, name: str = 'AggregateStep', description: str = 'Aggregate data'):
        """
        初始化 AggregateStep。

        Args:
            name (str): 步骤名称。
            description (str): 步骤描述。
        """
        self.name = name
        self.description = description
        self.config = None
        self.sources = []
        self.destination = None
        self.aggregation_functions = {}

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

    def set_aggregation_functions(self, aggregation_functions: Dict[str, Any]) -> None:
        """
        设置聚合函数。

        Args:
            aggregation_functions (Dict[str, Any]): 聚合函数字典，键为字段名，值为聚合函数。
        """
        self.aggregation_functions = aggregation_functions

    def get_aggregation_functions(self) -> Dict[str, Any]:
        """
        获取聚合函数。

        Returns:
            Dict[str, Any]: 聚合函数字典。
        """
        return self.aggregation_functions

    def execute(self) -> None:
        """
        执行聚合步骤。

        对数据进行聚合操作，如求和、平均值等。
        """
        aggregated_data = {}
        for source in self.sources:
            if source.is_file():
                data = source.get_data()
                if isinstance(data, list):
                    for item in data:
                        for field, func in self.aggregation_functions.items():
                            if field in item:
                                if field not in aggregated_data:
                                    aggregated_data[field] = []
                                aggregated_data[field].append(item[field])

        result = {}
        for field, values in aggregated_data.items():
            func = self.aggregation_functions.get(field)
            if func:
                result[field] = func(values)

        self.destination.write(result)

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