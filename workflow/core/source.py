from typing import Any, List
import os
import requests

from workflow.interfaces.loader_interface import LoaderInterface
from workflow.interfaces.source_interface import SourceInterface


class Source(SourceInterface):
    """
    数据源类。

    表示数据的来源，可以是文件、目录、URL 等。
    """

    def __init__(self, path: str, type: str, data: Any = None):
        """
        初始化 Source。

        Args:
            path (str): 数据源路径。
            type (str): 数据源类型，可以是 'file'、'dir'、'url' 等。
            data (Any): 数据源的数据。默认为 None。
        """
        self.path = path
        self.type = type
        self.data = data

    def load(self, loader: 'LoaderInterface') -> None:
        """
        使用指定的加载器加载数据源。

        Args:
            loader (LoaderInterface): 加载器对象。
        """
        self.data = loader.load(self.path)

    def get_data(self) -> Any:
        """
        获取数据源的数据。

        Returns:
            Any: 数据源的数据。
        """
        return self.data

    def set_data(self, data: Any) -> None:
        """
        设置数据源的数据。

        Args:
            data (Any): 要设置的数据。
        """
        self.data = data

    def get_path(self) -> str:
        """
        获取数据源的路径。

        Returns:
            str: 数据源的路径。
        """
        return self.path

    def set_path(self, path: str) -> None:
        """
        设置数据源的路径。

        Args:
            path (str): 数据源的路径。
        """
        self.path = path

    def get_name(self) -> str:
        """
        获取数据源的名称。

        Returns:
            str: 数据源的名称。
        """
        return os.path.basename(self.path)

    def set_name(self, name: str) -> None:
        """
        设置数据源的名称。

        Args:
            name (str): 数据源的名称。
        """
        base, ext = os.path.splitext(self.path)
        self.path = os.path.join(os.path.dirname(self.path), f"{name}{ext}")

    def get_type(self) -> str:
        """
        获取数据源的类型。

        Returns:
            str: 数据源的类型。
        """
        return self.type

    def set_type(self, type: str) -> None:
        """
        设置数据源的类型。

        Args:
            type (str): 数据源的类型。
        """
        self.type = type

    def exists(self) -> bool:
        """
        检查数据源是否存在。

        Returns:
            bool: 如果数据源存在，则返回 True，否则返回 False。
        """
        if self.type == 'url':
            try:
                response = requests.head(self.path)
                return response.status_code == 200
            except requests.exceptions.RequestException:
                return False
        return os.path.exists(self.path)

    def is_file(self) -> bool:
        """
        检查数据源是否为文件。

        Returns:
            bool: 如果数据源是文件，则返回 True，否则返回 False。
        """
        return self.type == 'file' and os.path.isfile(self.path)

    def is_dir(self) -> bool:
        """
        检查数据源是否为目录。

        Returns:
            bool: 如果数据源是目录，则返回 True，否则返回 False。
        """
        return self.type == 'dir' and os.path.isdir(self.path)

    def is_url(self) -> bool:
        """
        检查数据源是否为 URL。

        Returns:
            bool: 如果数据源是 URL，则返回 True，否则返回 False。
        """
        return self.type == 'url'

    def get_files(self, pattern: str = None) -> List['SourceInterface']:
        """
        获取数据源中符合指定模式的文件。

        Args:
            pattern (str): 文件模式，可以包含通配符。默认为 None，表示获取所有文件。

        Returns:
            List[SourceInterface]: 符合指定模式的文件列表。
        """
        if not self.is_dir():
            return []
        files = []
        for entry in os.listdir(self.path):
            entry_path = os.path.join(self.path, entry)
            if os.path.isfile(entry_path) and (not pattern or entry.endswith(pattern)):
                files.append(Source(entry_path, 'file'))
        return files

    def get_dirs(self, pattern: str = None) -> List['SourceInterface']:
        """
        获取数据源中符合指定模式的目录。

        Args:
            pattern (str): 目录模式，可以包含通配符。默认为 None，表示获取所有目录。

        Returns:
            List[SourceInterface]: 符合指定模式的目录列表。
        """
        if not self.is_dir():
            return []
        dirs = []
        for entry in os.listdir(self.path):
            entry_path = os.path.join(self.path, entry)
            if os.path.isdir(entry_path) and (not pattern or entry.endswith(pattern)):
                dirs.append(Source(entry_path, 'dir'))
        return dirs

    def get_urls(self, pattern: str = None) -> List['SourceInterface']:
        """
        获取数据源中符合指定模式的 URL。

        Args:
            pattern (str): URL 模式，可以包含通配符。默认为 None，表示获取所有 URL。

        Returns:
            List[SourceInterface]: 符合指定模式的 URL 列表。
        """
        if not self.is_url():
            return []
        return [self] if not pattern or self.path.endswith(pattern) else []

    def get_all(self, pattern: str = None) -> List['SourceInterface']:
        """
        获取数据源中符合指定模式的所有文件、目录和 URL。

        Args:
            pattern (str): 文件、目录和 URL 模式，可以包含通配符。默认为 None，表示获取所有。

        Returns:
            List[SourceInterface]: 符合指定模式的文件、目录和 URL 列表。
        """
        if self.is_file():
            return [self] if not pattern or self.path.endswith(pattern) else []
        elif self.is_dir():
            return self.get_files(pattern) + self.get_dirs(pattern)
        elif self.is_url():
            return self.get_urls(pattern)
        return []
