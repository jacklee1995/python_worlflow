from abc import ABC, abstractmethod
from typing import List

from intefaces.config import Config
from intefaces.source import Source


class Step(ABC):
    """
    步骤接口。

    步骤表示任务执行过程中的一个原子操作或阶段。一个任务可以由一个或多个步骤组成。

    Attributes:
        name (str): 步骤名称。
        description (str): 步骤描述。

    Methods:
        execute(sources: List[Source], config: Config) -> None:
            执行步骤。

        set_name(name: str) -> None:
            设置步骤名称。

        get_name() -> str:
            获取步骤名称。

        set_description(description: str) -> None:
            设置步骤描述。

        get_description() -> str:
            获取步骤描述。
    """

    @abstractmethod
    def execute(self, sources: List[Source], config: Config) -> None:
        """
        执行步骤。

        Args:
            sources (List[Source]): 步骤执行所需的资源列表。
            config (Config): 步骤执行的配置。

        Returns:
            None
        """
        pass

    @abstractmethod
    def set_name(self, name: str) -> None:
        """
        设置步骤名称。

        Args:
            name (str): 步骤名称。

        Returns:
            None
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """
        获取步骤名称。

        Returns:
            str: 步骤名称。
        """
        pass

    @abstractmethod
    def set_description(self, description: str) -> None:
        """
        设置步骤描述。

        Args:
            description (str): 步骤描述。

        Returns:
            None
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