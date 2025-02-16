from typing import List
import os
import json
import yaml
import xml.etree.ElementTree as ET

from workflow.interfaces.step_interface import StepInterface
from workflow.interfaces.source_interface import SourceInterface
from workflow.interfaces.destination_interface import DestinationInterface
from workflow.interfaces.config_interface import ConfigInterface


class ValidateStep(StepInterface):
    """
    验证步骤。

    用于验证文件或数据的格式是否符合预期。
    """

    def __init__(self, name: str = 'ValidateStep', description: str = 'Validate file or data format'):
        """
        初始化 ValidateStep。

        Args:
            name (str): 步骤名称。
            description (str): 步骤描述。
        """
        self.name = name
        self.description = description
        self.config = None
        self.sources = []
        self.destination = None
        self.format = 'json'  # 默认验证格式为 JSON

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

    def set_format(self, format: str) -> None:
        """
        设置验证的格式。

        Args:
            format (str): 验证的格式，如 'json', 'yaml', 'xml' 等。
        """
        self.format = format

    def get_format(self) -> str:
        """
        获取验证的格式。

        Returns:
            str: 验证的格式。
        """
        return self.format

    def execute(self) -> None:
        """
        执行验证步骤。

        验证文件或数据的格式是否符合预期。
        """
        for source in self.sources:
            if source.is_file():
                path = source.get_path()
                try:
                    if self.format == 'json':
                        with open(path, 'r') as f:
                            json.load(f)
                    elif self.format == 'yaml':
                        with open(path, 'r') as f:
                            yaml.safe_load(f)
                    elif self.format == 'xml':
                        ET.parse(path)
                    else:
                        raise ValueError(f"Unsupported format: {self.format}")
                except Exception as e:
                    raise ValueError(f"Validation failed for {path}: {str(e)}")

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