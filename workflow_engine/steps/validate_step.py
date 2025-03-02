from typing import List
import os
import json
import yaml
import xml.etree.ElementTree as ET

from workflow_engine.interfaces.step_interface import StepInterface
from workflow_engine.interfaces.source_interface import SourceInterface
from workflow_engine.interfaces.output_interface import OutputInterface
from workflow_engine.interfaces.config_interface import ConfigInterface


class ValidateStep(StepInterface):
    """
    验证步骤。

    用于验证文件或数据的格式是否符合预期。
    """

    def __init__(self, name: str = 'ValidateStep', description: str = 'Validate file or data format'):
        """
        初始化ValidateStep。

        Args:
            name (str): 步骤名称。
            description (str): 步骤描述。
        """
        self.name = name
        self.description = description
        self.config = None
        self.sources = []
        self.output = None
        self.format = 'json'  # 默认验证格式为JSON

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

    def set_format(self, format: str) -> None:
        """
        设置验证的格式。

        Args:
            format (str): 验证的格式,如'json', 'yaml', 'xml'等。
        """
        self.format = format

    def get_format(self) -> str:
        """
        获取验证的格式。

        Returns:
            str: 验证的格式。
        """
        return self.format

    async def execute(self) -> None:
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
                    
                    if self.output:
                        await self.output.write(f"Validation successful for {path}".encode())
                except Exception as e:
                    if self.output:
                        await self.output.write(f"Validation failed for {path}: {str(e)}".encode())
                    raise ValueError(f"Validation failed for {path}: {str(e)}")

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