from abc import ABC, abstractmethod
from typing import Any, List


class LoaderInterface(ABC):
    """
    加载器接口。

    加载器用于加载不同类型的资源，如文件、目录、URL等。
    """

    @abstractmethod
    def load(self, path: str) -> Any:
        """
        加载指定路径的资源。

        Args:
            path (str): 资源路径。

        Returns:
            Any: 加载后的资源对象。
        """
        pass

    @abstractmethod
    def get_extensions(self) -> List[str]:
        """
        获取加载器支持的文件扩展名列表。

        Returns:
            List[str]: 支持的文件扩展名列表。
        """
        pass

    @abstractmethod
    def set_extensions(self, extensions: List[str]) -> None:
        """
        设置加载器支持的文件扩展名列表。

        Args:
            extensions (List[str]): 支持的文件扩展名列表。
        """
        pass

    @abstractmethod
    def get_type(self) -> str:
        """
        获取加载器的类型。

        Returns:
            str: 加载器的类型。
        """
        pass

    @abstractmethod
    def set_type(self, loader_type: str) -> None:
        """
        设置加载器的类型。

        Args:
            loader_type (str): 加载器的类型。
        """
        pass

    @abstractmethod
    def get_options(self) -> dict:
        """
        获取加载器的选项。

        Returns:
            dict: 加载器的选项。
        """
        pass

    @abstractmethod
    def set_options(self, options: dict) -> None:
        """
        设置加载器的选项。

        Args:
            options (dict): 加载器的选项。
        """
        pass

    @abstractmethod
    def is_supported(self, path: str) -> bool:
        """
        判断加载器是否支持指定路径的资源。

        Args:
            path (str): 资源路径。

        Returns:
            bool: 如果支持，返回 True；否则返回 False。
        """
        pass

    @abstractmethod
    def transform(self, data: Any) -> Any:
        """
        对加载后的资源进行转换。

        Args:
            data (Any): 加载后的资源对象。

        Returns:
            Any: 转换后的资源对象。
        """
        pass