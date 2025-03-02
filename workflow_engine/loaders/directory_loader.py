from typing import Any, List
import os

from workflow_engine.interfaces.loader_interface import LoaderInterface
from workflow_engine.interfaces.source_interface import SourceInterface
from workflow_engine.core.source import Source


class DirectoryLoader(LoaderInterface):
    """
    目录加载器。

    用于加载目录中的文件和子目录。
    """

    def __init__(self, recursive: bool = True):
        """
        初始化 DirectoryLoader。

        Args:
            recursive (bool): 是否递归加载子目录。默认为 True。
        """
        self.recursive = recursive
        self.extensions = []
        self.type = 'directory'
        self.options = {}

    def load(self, path: str) -> List[SourceInterface]:
        """
        加载指定目录中的文件和子目录。

        Args:
            path (str): 目录路径。

        Returns:
            List[SourceInterface]: 加载后的文件和子目录列表。
        """
        sources = []

        if not os.path.isdir(path):
            raise ValueError(f"{path} is not a valid directory.")

        for entry in os.listdir(path):
            entry_path = os.path.join(path, entry)

            if os.path.isfile(entry_path):
                if self.is_supported(entry_path):
                    source = Source(entry_path, 'file')
                    sources.append(source)
            elif os.path.isdir(entry_path) and self.recursive:
                sub_sources = self.load(entry_path)
                sources.extend(sub_sources)

        return sources

    def get_extensions(self) -> List[str]:
        """
        获取支持的文件扩展名列表。

        Returns:
            List[str]: 支持的文件扩展名列表。
        """
        return self.extensions

    def set_extensions(self, extensions: List[str]) -> None:
        """
        设置支持的文件扩展名列表。

        Args:
            extensions (List[str]): 支持的文件扩展名列表。
        """
        self.extensions = extensions

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
        判断是否支持加载指定路径的文件。

        Args:
            path (str): 文件路径。

        Returns:
            bool: 如果支持，返回 True；否则返回 False。
        """
        _, extension = os.path.splitext(path)
        return extension in self.extensions

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。

        Args:
            data (Any): 加载后的数据。

        Returns:
            Any: 转换后的数据。
        """
        return data