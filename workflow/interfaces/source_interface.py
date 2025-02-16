from abc import ABC, abstractmethod
from typing import Any, List

from .loader_interface import LoaderInterface

class SourceInterface(ABC):
    """
    数据源接口。

    数据源表示数据的来源，可以是文件、目录、URL 等。
    """

    @abstractmethod
    def load(self, loader: 'LoaderInterface') -> None:
        """
        使用指定的加载器加载数据源。

        Args:
            loader (LoaderInterface): 加载器对象。
        """
        pass

    @abstractmethod
    def get_data(self) -> Any:
        """
        获取数据源的数据。

        Returns:
            Any: 数据源的数据。
        """
        pass

    @abstractmethod
    def set_data(self, data: Any) -> None:
        """
        设置数据源的数据。

        Args:
            data (Any): 要设置的数据。
        """
        pass

    @abstractmethod
    def get_path(self) -> str:
        """
        获取数据源的路径。

        Returns:
            str: 数据源的路径。
        """
        pass

    @abstractmethod
    def set_path(self, path: str) -> None:
        """
        设置数据源的路径。

        Args:
            path (str): 数据源的路径。
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """
        获取数据源的名称。

        Returns:
            str: 数据源的名称。
        """
        pass

    @abstractmethod
    def set_name(self, name: str) -> None:
        """
        设置数据源的名称。

        Args:
            name (str): 数据源的名称。
        """
        pass

    @abstractmethod
    def get_type(self) -> str:
        """
        获取数据源的类型。

        Returns:
            str: 数据源的类型。
        """
        pass

    @abstractmethod
    def set_type(self, type: str) -> None:
        """
        设置数据源的类型。

        Args:
            type (str): 数据源的类型。
        """
        pass

    @abstractmethod
    def exists(self) -> bool:
        """
        检查数据源是否存在。

        Returns:
            bool: 如果数据源存在，则返回 True，否则返回 False。
        """
        pass

    @abstractmethod
    def is_file(self) -> bool:
        """
        检查数据源是否为文件。

        Returns:
            bool: 如果数据源是文件，则返回 True，否则返回 False。
        """
        pass

    @abstractmethod
    def is_dir(self) -> bool:
        """
        检查数据源是否为目录。

        Returns:
            bool: 如果数据源是目录，则返回 True，否则返回 False。
        """
        pass

    @abstractmethod
    def is_url(self) -> bool:
        """
        检查数据源是否为 URL。

        Returns:
            bool: 如果数据源是 URL，则返回 True，否则返回 False。
        """
        pass

    @abstractmethod
    def get_files(self, pattern: str = None) -> List['SourceInterface']:
        """
        获取数据源中符合指定模式的文件。

        Args:
            pattern (str): 文件模式，可以包含通配符。默认为 None，表示获取所有文件。

        Returns:
            List[SourceInterface]: 符合指定模式的文件列表。
        """
        pass

    @abstractmethod
    def get_dirs(self, pattern: str = None) -> List['SourceInterface']:
        """
        获取数据源中符合指定模式的目录。

        Args:
            pattern (str): 目录模式，可以包含通配符。默认为 None，表示获取所有目录。

        Returns:
            List[SourceInterface]: 符合指定模式的目录列表。
        """
        pass

    @abstractmethod
    def get_urls(self, pattern: str = None) -> List['SourceInterface']:
        """
        获取数据源中符合指定模式的 URL。

        Args:
            pattern (str): URL 模式，可以包含通配符。默认为 None，表示获取所有 URL。

        Returns:
            List[SourceInterface]: 符合指定模式的 URL 列表。
        """
        pass

    @abstractmethod
    def get_all(self, pattern: str = None) -> List['SourceInterface']:
        """
        获取数据源中符合指定模式的所有文件、目录和 URL。

        Args:
            pattern (str): 文件、目录和 URL 模式，可以包含通配符。默认为 None，表示获取所有。

        Returns:
            List[SourceInterface]: 符合指定模式的文件、目录和 URL 列表。
        """
        pass