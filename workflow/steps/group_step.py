from typing import List, Dict, Any
import os
import shutil

from workflow.interfaces.step_interface import StepInterface
from workflow.interfaces.source_interface import SourceInterface
from workflow.interfaces.destination_interface import DestinationInterface
from workflow.interfaces.config_interface import ConfigInterface


class GroupStep(StepInterface):
    """
    分组步骤。

    根据指定条件对文件或数据进行分组。
    """

    def __init__(self, name: str = 'GroupStep', description: str = 'Group files or data'):
        """
        初始化 GroupStep。

        Args:
            name (str): 步骤名称。
            description (str): 步骤描述。
        """
        self.name = name
        self.description = description
        self.config = None
        self.sources = []
        self.destination = None
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

    def execute(self) -> None:
        """
        执行分组步骤。

        根据指定条件对文件或数据进行分组。
        """
        if not self.group_by:
            raise ValueError("Group by condition is not set.")

        grouped_data: Dict[str, List[Any]] = {}

        for source in self.sources:
            if source.is_file():
                # 根据文件名或其他属性进行分组
                key = self._get_group_key(source.get_path())
                if key not in grouped_data:
                    grouped_data[key] = []
                grouped_data[key].append(source.get_path())

        # 将分组结果保存到目标目录
        dest_path = self.destination.get_path()
        os.makedirs(dest_path, exist_ok=True)

        for key, files in grouped_data.items():
            group_dir = os.path.join(dest_path, key)
            os.makedirs(group_dir, exist_ok=True)

            for file in files:
                shutil.copy(file, group_dir)

    def _get_group_key(self, path: str) -> str:
        """
        根据分组条件获取分组键。

        Args:
            path (str): 文件路径。

        Returns:
            str: 分组键。
        """
        if self.group_by == 'extension':
            return os.path.splitext(path)[1][1:]  # 去掉点号
        elif self.group_by == 'name':
            return os.path.basename(path).split('.')[0]
        else:
            raise ValueError(f"Unsupported group by condition: {self.group_by}")

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