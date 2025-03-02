from typing import List
import re

from workflow_engine.interfaces.step_interface import StepInterface
from workflow_engine.interfaces.source_interface import SourceInterface
from workflow_engine.interfaces.output_interface import OutputInterface
from workflow_engine.interfaces.config_interface import ConfigInterface


class ReplaceStep(StepInterface):
    """
    替换步骤。

    对源文件中的内容进行替换操作。
    """

    def __init__(self, name: str = 'ReplaceStep', description: str = 'Replace content in files'):
        """
        初始化ReplaceStep。

        Args:
            name (str): 步骤名称。
            description (str): 步骤描述。
        """
        self.name = name
        self.description = description
        self.config = None
        self.sources = []
        self.output = None
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

    async def execute(self) -> None:
        """
        执行替换步骤。

        对源文件中的内容进行替换操作。
        """
        for source in self.sources:
            async for data in source.read_chunks():
                if isinstance(data, bytes):
                    content = data.decode('utf-8')
                    replaced = re.sub(self.pattern, self.replacement, content)
                    await self.output.write(replaced.encode('utf-8'))

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