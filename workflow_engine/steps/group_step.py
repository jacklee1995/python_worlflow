from typing import List, Dict, Any
import os
import shutil

from workflow_engine.interfaces.step_interface import StepInterface
from workflow_engine.interfaces.source_interface import SourceInterface
from workflow_engine.interfaces.output_interface import OutputInterface
from workflow_engine.interfaces.config_interface import ConfigInterface


class GroupStep(StepInterface):
    """
    分组步骤。

    根据指定条件对文件或数据进行分组。
    """

    def __init__(self, name: str = 'GroupStep', description: str = 'Group files or data'):
        """
        初始化GroupStep。

        Args:
            name (str): 步骤名称。
            description (str): 步骤描述。
        """
        self.name = name
        self.description = description
        self.config = None
        self.sources = []
        self.output = None
        self.group_by = None

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

    def set_group_by(self, group_by: str) -> None:
        """
        设置分组条件。

        Args:
            group_by (str): 分组条件。
        """
        self.group_by = group_by

    def get_group_by(self) -> str:
        """
        获取分组条件。

        Returns:
            str: 分组条件。
        """
        return self.group_by

    async def execute(self) -> None:
        """
        执行分组步骤。

        根据指定条件对文件或数据进行分组。
        """
        if not self.group_by:
            raise ValueError("Group by condition is not set.")

        grouped_data: Dict[str, List[Any]] = {}

        for source in self.sources:
            async for data in source.read_chunks():
                key = self._get_group_key(data)
                if key not in grouped_data:
                    grouped_data[key] = []
                grouped_data[key].append(data)

        # 将分组结果写入输出
        if self.output:
            await self.output.write(grouped_data)

    def _get_group_key(self, data: bytes) -> str:
        """
        根据分组条件获取分组键。

        Args:
            data (bytes): 数据。

        Returns:
            str: 分组键。
        """
        try:
            decoded_data = data.decode('utf-8')
            if self.group_by == 'extension':
                return os.path.splitext(decoded_data)[1][1:]  # 去掉点号
            elif self.group_by == 'name':
                return os.path.basename(decoded_data).split('.')[0]
            else:
                raise ValueError(f"Unsupported group by condition: {self.group_by}")
        except Exception:
            return 'unknown'

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