from typing import Any
from workflow.interfaces.loader_interface import LoaderInterface
from workflow.core.source import Source

class BinaryLoader(LoaderInterface):
    """
    二进制加载器。
    
    用于加载二进制文件（如 PDF、DOCX 等），并将其作为字节流返回。
    """

    def __init__(self):
        self.type = 'binary'
        self.options = {}

    def load(self, path: str) -> Source:
        """
        加载指定路径的二进制文件。

        Args:
            path (str): 二进制文件路径。

        Returns:
            Source: 加载后的二进制源对象。
        """
        with open(path, 'rb') as f:
            binary_data = f.read()
        return Source(path, 'binary', binary_data)

    def is_supported(self, path: str) -> bool:
        """
        判断是否支持加载指定路径的二进制文件。

        Args:
            path (str): 文件路径。

        Returns:
            bool: 如果支持，返回 True；否则返回 False。
        """
        return path.endswith(('.pdf', '.docx', '.xlsx', '.bin'))

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。

        Args:
            data (Any): 加载后的数据。

        Returns:
            Any: 转换后的数据。
        """
        return data
