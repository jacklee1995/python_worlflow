from typing import Any, List
import os

from workflow_engine.interfaces.loader_interface import LoaderInterface
from workflow_engine.interfaces.source_interface import SourceInterface
from workflow_engine.core.source import Source


class FileLoader(LoaderInterface):
    """
    文件加载器。

    用于加载单个文件。
    """

    def __init__(self, allowed_extensions: List[str] = None):
        """
        初始化 FileLoader。

        Args:
            allowed_extensions (List[str]): 允许加载的文件扩展名列表。默认为 None，表示允许所有扩展名。
        """
        self.allowed_extensions = allowed_extensions or []
        self.type = 'file'
        self.options = {}

    def load(self, path: str) -> SourceInterface:
        """
        加载指定路径的文件。

        Args:
            path (str): 文件路径。

        Returns:
            SourceInterface: 加载后的文件源对象。

        Raises:
            ValueError: 如果文件路径不存在或不是文件。
            ValueError: 如果文件扩展名不在允许的扩展名列表中。
        """
        if not os.path.exists(path):
            raise ValueError(f"{path} does not exist.")

        if not os.path.isfile(path):
            raise ValueError(f"{path} is not a valid file.")

        if not self.is_supported(path):
            raise ValueError(f"Unsupported file extension for {path}.")

        source = Source(path, 'file')
        return source

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
        判断是否支持加载指定路径的文件。

        Args:
            path (str): 文件路径。

        Returns:
            bool: 如果支持，返回 True；否则返回 False。
        """
        _, extension = os.path.splitext(path)
        return extension in self.allowed_extensions or not self.allowed_extensions

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。

        Args:
            data (Any): 加载后的数据。

        Returns:
            Any: 转换后的数据。
        """
        return data