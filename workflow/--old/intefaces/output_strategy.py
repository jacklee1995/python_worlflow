from abc import ABC, abstractmethod
from typing import Any


class OutputStrategy(ABC):
    """
    输出策略接口。

    输出策略定义了将数据输出到特定目标的方法。输出是任务执行的副作用或结果。

    Attributes:
        target (str): 输出的目标。

    Methods:
        output(data: Any) -> None:
            将数据输出到指定目标。

        set_target(target: str) -> None:
            设置输出的目标。

        get_target() -> str:
            获取输出的目标。
    """

    def __init__(self, target: str):
        """
        初始化 OutputStrategy 实例。

        Args:
            target (str): 输出的目标。
        """
        self.target = target

    @abstractmethod
    def output(self, data: Any) -> None:
        """
        将数据输出到指定目标。

        Args:
            data (Any): 要输出的数据。

        Returns:
            None
        """
        pass

    def set_target(self, target: str) -> None:
        """
        设置输出的目标。

        Args:
            target (str): 输出的目标。

        Returns:
            None
        """
        self.target = target

    def get_target(self) -> str:
        """
        获取输出的目标。

        Returns:
            str: 输出的目标。
        """
        return self.target