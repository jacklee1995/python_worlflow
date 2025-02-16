import time
from typing import List

from workflow.interfaces.step_interface import StepInterface
from workflow.interfaces.source_interface import SourceInterface
from workflow.interfaces.destination_interface import DestinationInterface
from workflow.interfaces.config_interface import ConfigInterface


class WaitStep(StepInterface):
    """
    等待步骤。

    等待指定的时间或条件。
    """

    def __init__(self, name: str = 'WaitStep', description: str = 'Wait for a specified time or condition'):
        """
        初始化 WaitStep。

        Args:
            name (str): 步骤名称。
            description (str): 步骤描述。
        """
        self.name = name
        self.description = description
        self.config = None
        self.sources = []
        self.destination = None
        self.wait_time = 0

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

    def set_wait_time(self, wait_time: int) -> None:
        """
        设置等待时间。

        Args:
            wait_time (int): 等待时间（秒）。
        """
        self.wait_time = wait_time

    def get_wait_time(self) -> int:
        """
        获取等待时间。

        Returns:
            int: 等待时间（秒）。
        """
        return self.wait_time

    def execute(self) -> None:
        """
        执行等待步骤。

        等待指定的时间。
        """
        time.sleep(self.wait_time)

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