from abc import ABC, abstractmethod
from typing import Any


class LoadStrategy(ABC):
    """
    加载策略接口。

    加载策略定义了从特定源加载数据的方法。不同的具体资源可以有自己的加载方式，通过实现加载策略接口，可以使用不同的策略来实现具体的资源加载。

    Attributes:
        source (str): 加载数据的源。

    Methods:
        load() -> Any:
            从指定源加载数据。

        set_source(source: str) -> None:
            设置加载数据的源。

        get_source() -> str:
            获取加载数据的源。
    """

    def __init__(self, source: str):
        """
        初始化 LoadStrategy 实例。

        Args:
            source (str): 加载数据的源。
        """
        self.source = source

    @abstractmethod
    def load(self) -> Any:
        """
        从指定源加载数据。

        Returns:
            Any: 加载的数据。
        """
        pass

    def set_source(self, source: str) -> None:
        """
        设置加载数据的源。

        Args:
            source (str): 加载数据的源。

        Returns:
            None
        """
        self.source = source

    def get_source(self) -> str:
        """
        获取加载数据的源。

        Returns:
            str: 加载数据的源。
        """
        return self.source