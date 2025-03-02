from typing import List, Callable
from workflow_engine.interfaces.step_interface import StepInterface
from workflow_engine.interfaces.source_interface import SourceInterface
from workflow_engine.interfaces.output_interface import OutputInterface
from workflow_engine.interfaces.config_interface import ConfigInterface


class ConditionStep(StepInterface):
    """
    条件步骤。

    根据条件判断是否执行后续步骤。
    """

    def __init__(self, name: str = 'ConditionStep', description: str = 'Conditional execution'):
        """
        初始化 ConditionStep。

        Args:
            name (str): 步骤名称。
            description (str): 步骤描述。
        """
        self.name = name
        self.description = description
        self.config = None
        self.sources = []
        self.output = None
        self.condition: Callable[[], bool] = lambda: True

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
            sources (List[SourceInterface]: 步骤的数据源列表。
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
        设置步骤的输出目标。

        Args:
            output (OutputInterface): 步骤的输出目标。
        """
        self.output = output

    def get_output(self) -> OutputInterface:
        """
        获取步骤的输出目标。

        Returns:
            OutputInterface: 步骤的输出目标。
        """
        return self.output

    def set_condition(self, condition: Callable[[], bool]) -> None:
        """
        设置条件函数。

        Args:
            condition (Callable[[], bool]): 条件函数，返回布尔值。
        """
        self.condition = condition

    def get_condition(self) -> Callable[[], bool]:
        """
        获取条件函数。

        Returns:
            Callable[[], bool]: 条件函数。
        """
        return self.condition

    def execute(self) -> None:
        """
        执行条件步骤。

        根据条件判断是否执行后续步骤。
        """
        if self.condition():
            for source in self.sources:
                if self.output:
                    source.copy(self.output)

    def pipe(self, step: StepInterface) -> StepInterface:
        """
        将当前步骤的输出连接到另一个步骤的输入。

        Args:
            step (StepInterface): 下一个步骤。

        Returns:
            StepInterface: 下一个步骤。
        """
        if self.condition():
            step.set_sources([self.output])
        return step 