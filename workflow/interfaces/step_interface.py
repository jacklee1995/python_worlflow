from abc import ABC, abstractmethod
from typing import List, Union

from .config_interface import ConfigInterface
from .source_interface import SourceInterface
from .destination_interface import DestinationInterface


class StepInterface(ABC):
    """
    步骤接口。

    步骤表示任务执行过程中的一个原子操作或阶段。一个任务可以由一个或多个步骤组成。
    """

    @abstractmethod
    def get_name(self) -> str:
        """
        获取步骤名称。

        Returns:
            str: 步骤名称。
        """
        pass

    @abstractmethod
    def set_name(self, name: str) -> None:
        """
        设置步骤名称。

        Args:
            name (str): 步骤名称。
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """
        获取步骤描述。

        Returns:
            str: 步骤描述。
        """
        pass

    @abstractmethod
    def set_description(self, description: str) -> None:
        """
        设置步骤描述。

        Args:
            description (str): 步骤描述。
        """
        pass

    @abstractmethod
    def set_config(self, config: ConfigInterface) -> None:
        """
        设置步骤的配置。

        Args:
            config (ConfigInterface): 步骤的配置。
        """
        pass

    @abstractmethod
    def get_config(self) -> ConfigInterface:
        """
        获取步骤的配置。

        Returns:
            ConfigInterface: 步骤的配置。
        """
        pass

    @abstractmethod
    def set_sources(self, sources: List[SourceInterface]) -> None:
        """
        设置步骤的数据源。

        Args:
            sources (List[SourceInterface]): 步骤的数据源列表。
        """
        pass

    @abstractmethod
    def get_sources(self) -> List[SourceInterface]:
        """
        获取步骤的数据源。

        Returns:
            List[SourceInterface]: 步骤的数据源列表。
        """
        pass

    @abstractmethod
    def set_destination(self, destination: DestinationInterface) -> None:
        """
        设置步骤的输出目标。

        Args:
            destination (DestinationInterface): 步骤的输出目标。
        """
        pass

    @abstractmethod
    def get_destination(self) -> DestinationInterface:
        """
        获取步骤的输出目标。

        Returns:
            DestinationInterface: 步骤的输出目标。
        """
        pass

    @abstractmethod
    def execute(self) -> None:
        """
        执行步骤。
        """
        pass

    @abstractmethod
    def pipe(self, step: 'StepInterface') -> 'StepInterface':
        """
        将当前步骤的输出连接到另一个步骤的输入。

        Args:
            step (StepInterface): 下一个步骤。

        Returns:
            StepInterface: 下一个步骤。
        """
        pass