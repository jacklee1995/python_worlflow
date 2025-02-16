from typing import List
import re

from workflow.interfaces.step_interface import StepInterface
from workflow.interfaces.source_interface import SourceInterface
from workflow.interfaces.destination_interface import DestinationInterface
from workflow.interfaces.config_interface import ConfigInterface


class ReplaceStep(StepInterface):
    """
    替换步骤。

    对源文件中的内容进行替换操作。
    """

    def __init__(self, name: str = 'ReplaceStep', description: str = 'Replace content in files'):
        """
        初始化 ReplaceStep。

        Args:
            name (str): 步骤名称。
            description (str): 步骤描述。
        """
        self.name = name
        self.description = description
        self.config = None
        self.sources = []
        self.destination = None
        self.pattern = ''
        self.replacement = ''

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

    def set_pattern(self, pattern: str) -> None:
        """
        设置替换的正则表达式模式。

        Args:
            pattern (str): 正则表达式模式。
        """
        self.pattern = pattern

    def get_pattern(self) -> str:
        """
        获取替换的正则表达式模式。

        Returns:
            str: 正则表达式模式。
        """
        return self.pattern

    def set_replacement(self, replacement: str) -> None:
        """
        设置替换的内容。

        Args:
            replacement (str): 替换的内容。
        """
        self.replacement = replacement

    def get_replacement(self) -> str:
        """
        获取替换的内容。

        Returns:
            str: 替换的内容。
        """
        return self.replacement

    def execute(self) -> None:
        """
        执行替换步骤。

        对源文件中的内容进行替换操作。
        """
        for source in self.sources:
            if source.is_file():
                with open(source.get_path(), 'r') as file:
                    content = file.read()

                content = re.sub(self.pattern, self.replacement, content)

                with open(self.destination.get_path(), 'w') as file:
                    file.write(content)

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