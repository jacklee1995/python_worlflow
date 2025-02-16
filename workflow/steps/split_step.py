import os
from typing import List

from workflow.interfaces.step_interface import StepInterface
from workflow.interfaces.source_interface import SourceInterface
from workflow.interfaces.destination_interface import DestinationInterface
from workflow.interfaces.config_interface import ConfigInterface


class SplitStep(StepInterface):
    """
    分割步骤。

    将文件按指定大小或行数分割为多个文件。
    """

    def __init__(self, name: str = 'SplitStep', description: str = 'Split files'):
        """
        初始化 SplitStep。

        Args:
            name (str): 步骤名称。
            description (str): 步骤描述。
        """
        self.name = name
        self.description = description
        self.config = None
        self.sources = []
        self.destination = None
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

    def execute(self) -> None:
        """
        执行分割步骤。

        将文件按指定大小或行数分割为多个文件。
        """
        for source in self.sources:
            if source.is_file():
                src_path = source.get_path()
                dest_dir = self.destination.get_path()

                if self.split_size > 0:
                    self._split_by_size(src_path, dest_dir)
                elif self.split_lines > 0:
                    self._split_by_lines(src_path, dest_dir)

    def _split_by_size(self, src_path: str, dest_dir: str) -> None:
        """
        按大小分割文件。

        Args:
            src_path (str): 源文件路径。
            dest_dir (str): 目标目录路径。
        """
        with open(src_path, 'rb') as src_file:
            part_num = 1
            while True:
                chunk = src_file.read(self.split_size)
                if not chunk:
                    break

                dest_path = os.path.join(dest_dir, f"{os.path.basename(src_path)}.part{part_num}")
                with open(dest_path, 'wb') as dest_file:
                    dest_file.write(chunk)

                part_num += 1

    def _split_by_lines(self, src_path: str, dest_dir: str) -> None:
        """
        按行数分割文件。

        Args:
            src_path (str): 源文件路径。
            dest_dir (str): 目标目录路径。
        """
        with open(src_path, 'r') as src_file:
            part_num = 1
            lines = []
            for line in src_file:
                lines.append(line)
                if len(lines) >= self.split_lines:
                    dest_path = os.path.join(dest_dir, f"{os.path.basename(src_path)}.part{part_num}")
                    with open(dest_path, 'w') as dest_file:
                        dest_file.writelines(lines)
                    lines = []
                    part_num += 1

            if lines:
                dest_path = os.path.join(dest_dir, f"{os.path.basename(src_path)}.part{part_num}")
                with open(dest_path, 'w') as dest_file:
                    dest_file.writelines(lines)

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