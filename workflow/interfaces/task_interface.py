from abc import ABC, abstractmethod
from typing import List, Union

from .step_interface import StepInterface
from .config_interface import ConfigInterface
from .source_interface import SourceInterface
from .destination_interface import DestinationInterface


class TaskInterface(ABC):
    """
    任务接口。

    任务表示一个完整的工作单元，由一个或多个步骤组成。任务可以串行或并行执行。
    """

    @abstractmethod
    def get_name(self) -> str:
        """
        获取任务名称。

        Returns:
            str: 任务名称。
        """
        pass

    @abstractmethod
    def set_name(self, name: str) -> None:
        """
        设置任务名称。

        Args:
            name (str): 任务名称。
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """
        获取任务描述。

        Returns:
            str: 任务描述。
        """
        pass

    @abstractmethod
    def set_description(self, description: str) -> None:
        """
        设置任务描述。

        Args:
            description (str): 任务描述。
        """
        pass

    @abstractmethod
    def add_step(self, step: StepInterface) -> None:
        """
        添加步骤到任务中。

        Args:
            step (StepInterface): 要添加的步骤。
        """
        pass

    @abstractmethod
    def remove_step(self, step: StepInterface) -> None:
        """
        从任务中移除步骤。

        Args:
            step (StepInterface): 要移除的步骤。
        """
        pass

    @abstractmethod
    def get_steps(self) -> List[StepInterface]:
        """
        获取任务的所有步骤。

        Returns:
            List[StepInterface]: 任务的所有步骤。
        """
        pass

    @abstractmethod
    def set_config(self, config: ConfigInterface) -> None:
        """
        设置任务的配置。

        Args:
            config (ConfigInterface): 任务的配置。
        """
        pass

    @abstractmethod
    def get_config(self) -> ConfigInterface:
        """
        获取任务的配置。

        Returns:
            ConfigInterface: 任务的配置。
        """
        pass

    @abstractmethod
    def set_sources(self, sources: List[SourceInterface]) -> None:
        """
        设置任务的数据源。

        Args:
            sources (List[SourceInterface]): 任务的数据源列表。
        """
        pass

    @abstractmethod
    def get_sources(self) -> List[SourceInterface]:
        """
        获取任务的数据源。

        Returns:
            List[SourceInterface]: 任务的数据源列表。
        """
        pass

    @abstractmethod
    def set_destination(self, destination: DestinationInterface) -> None:
        """
        设置任务的输出目标。

        Args:
            destination (DestinationInterface): 任务的输出目标。
        """
        pass

    @abstractmethod
    def get_destination(self) -> DestinationInterface:
        """
        获取任务的输出目标。

        Returns:
            DestinationInterface: 任务的输出目标。
        """
        pass

    @abstractmethod
    def execute(self) -> None:
        """
        执行任务。
        """
        pass