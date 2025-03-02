from typing import Any, List
import os
import requests

from workflow_engine.interfaces.loader_interface import LoaderInterface
from workflow_engine.interfaces.source_interface import SourceInterface
from workflow_engine.core.source import Source

class Loader(LoaderInterface):
    """
    加载器基类。
    """

    def __init__(self, allowed_extensions: List[str] = None, allowed_schemes: List[str] = None):
        """
        初始化 Loader。

        Args:
            allowed_extensions (List[str]): 允许加载的文件扩展名列表。
            allowed_schemes (List[str]): 允许加载的 URL 协议列表。
        """
        self.allowed_extensions = allowed_extensions or []
        self.allowed_schemes = allowed_schemes or []
        self.type = 'base'
        self.options = {}

    def load(self, path: str) -> Any:
        """
        加载指定路径的资源。

        Args:
            path (str): 资源路径。

        Returns:
            Any: 加载后的资源对象。

        Raises:
            ValueError: 如果路径不支持。
        """
        if not self.is_supported(path):
            raise ValueError(f"Unsupported path: {path}")

        if self.type == 'file':
            return self._load_file(path)
        elif self.type == 'directory':
            return self._load_directory(path)
        elif self.type == 'url':
            return self._load_url(path)
        else:
            raise ValueError(f"Unknown loader type: {self.type}")

    def _load_file(self, path: str) -> SourceInterface:
        """
        加载文件。

        Args:
            path (str): 文件路径。

        Returns:
            SourceInterface: 加载后的文件源对象。
        """
        if not os.path.isfile(path):
            raise ValueError(f"{path} is not a valid file.")
        return Source(path, 'file')

    def _load_directory(self, path: str) -> List[SourceInterface]:
        """
        加载目录。

        Args:
            path (str): 目录路径。

        Returns:
            List[SourceInterface]: 加载后的文件和子目录列表。
        """
        if not os.path.isdir(path):
            raise ValueError(f"{path} is not a valid directory.")
        sources = []
        for entry in os.listdir(path):
            entry_path = os.path.join(path, entry)
            if os.path.isfile(entry_path):
                if self.is_supported(entry_path):
                    sources.append(Source(entry_path, 'file'))
            elif os.path.isdir(entry_path):
                sub_sources = self._load_directory(entry_path)
                sources.extend(sub_sources)
        return sources

    def _load_url(self, url: str) -> SourceInterface:
        """
        加载 URL。

        Args:
            url (str): 资源的 URL。

        Returns:
            SourceInterface: 加载后的资源对象。

        Raises:
            requests.exceptions.RequestException: 如果加载 URL 资源失败。
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return Source(url, 'url', response.text)
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Failed to load URL {url}. Error: {str(e)}")

    def get_extensions(self) -> List[str]:
        """
        获取允许加载的文件扩展名列表。

        Returns:
            List[str]: 允许加载的文件扩展名列表。
        """
        return self.allowed_extensions

    def set_extensions(self, extensions: List[str]) -> None:
        """
        设置允许加载的文件扩展名列表。

        Args:
            extensions (List[str]): 允许加载的文件扩展名列表。
        """
        self.allowed_extensions = extensions

    def get_type(self) -> str:
        """
        获取加载器的类型。

        Returns:
            str: 加载器的类型。
        """
        return self.type

    def set_type(self, loader_type: str) -> None:
        """
        设置加载器的类型。

        Args:
            loader_type (str): 加载器的类型。
        """
        self.type = loader_type

    def get_options(self) -> dict:
        """
        获取加载器的选项。

        Returns:
            dict: 加载器的选项。
        """
        return self.options

    def set_options(self, options: dict) -> None:
        """
        设置加载器的选项。

        Args:
            options (dict): 加载器的选项。
        """
        self.options = options

    def is_supported(self, path: str) -> bool:
        """
        判断是否支持加载指定路径的资源。

        Args:
            path (str): 资源路径。

        Returns:
            bool: 如果支持，返回 True；否则返回 False。
        """
        if self.type == 'file':
            _, ext = os.path.splitext(path)
            return ext in self.allowed_extensions or not self.allowed_extensions
        elif self.type == 'directory':
            return os.path.isdir(path)
        elif self.type == 'url':
            scheme = path.split('://')[0]
            return scheme in self.allowed_schemes or not self.allowed_schemes
        return False

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。

        Args:
            data (Any): 加载后的数据。

        Returns:
            Any: 转换后的数据。
        """
        return data
