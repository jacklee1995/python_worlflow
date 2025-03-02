import os
from typing import List

from workflow_engine.interfaces.step_interface import StepInterface
from workflow_engine.interfaces.source_interface import SourceInterface
from workflow_engine.interfaces.output_interface import OutputInterface
from workflow_engine.interfaces.config_interface import ConfigInterface


class SplitStep(StepInterface):
    """
    分割步骤。

    将文件按指定大小或行数分割为多个文件。
    """

    def __init__(self, name: str = 'SplitStep', description: str = 'Split files'):
        """
        初始化SplitStep。

        Args:
            name (str): 步骤名称。
            description (str): 步骤描述。
        """
        self.name = name
        self.description = description
        self.config = None
        self.sources = []
        self.output = None
        self.split_size = 0
        self.split_lines = 0

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

    def set_split_size(self, size: int) -> None:
        """
        设置分割大小（字节）。

        Args:
            size (int): 分割大小。
        """
        self.split_size = size

    def get_split_size(self) -> int:
        """
        获取分割大小。

        Returns:
            int: 分割大小。
        """
        return self.split_size

    def set_split_lines(self, lines: int) -> None:
        """
        设置分割行数。

        Args:
            lines (int): 分割行数。
        """
        self.split_lines = lines

    def get_split_lines(self) -> int:
        """
        获取分割行数。

        Returns:
            int: 分割行数。
        """
        return self.split_lines

    async def execute(self) -> None:
        """
        执行分割步骤。

        将文件按指定大小或行数分割为多个文件。
        """
        for source in self.sources:
            async for data in source.read_chunks():
                if self.split_size > 0:
                    await self._split_by_size(data)
                elif self.split_lines > 0:
                    await self._split_by_lines(data)

    async def _split_by_size(self, data: bytes) -> None:
        """
        按大小分割数据。

        Args:
            data (bytes): 要分割的数据。
        """
        start = 0
        part_num = 1
        while start < len(data):
            chunk = data[start:start + self.split_size]
            if not chunk:
                break

            await self.output.write(chunk)
            start += self.split_size
            part_num += 1

    async def _split_by_lines(self, data: bytes) -> None:
        """
        按行数分割数据。

        Args:
            data (bytes): 要分割的数据。
        """
        lines = data.splitlines(keepends=True)
        start = 0
        part_num = 1
        while start < len(lines):
            chunk = b''.join(lines[start:start + self.split_lines])
            if not chunk:
                break

            await self.output.write(chunk)
            start += self.split_lines
            part_num += 1

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