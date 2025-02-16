from typing import Any
from workflow.interfaces.loader_interface import LoaderInterface
from workflow.core.source import Source

class TextLoader(LoaderInterface):
    """
    文本加载器。
    
    用于加载纯文本文件，并将其作为字符串返回。
    """

    def __init__(self):
        self.type = 'text'
        self.options = {}

    def load(self, path: str) -> Source:
        """
        加载指定路径的文本文件。

        Args:
            path (str): 文本文件路径。

        Returns:
            Source: 加载后的文本源对象。
        """
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        return Source(path, 'text', text)

    def is_supported(self, path: str) -> bool:
        """
        判断是否支持加载指定路径的文本文件。

        Args:
            path (str): 文件路径。

        Returns:
            bool: 如果支持，返回 True；否则返回 False。
        """
        return path.endswith('.txt')

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。

        Args:
            data (Any): 加载后的数据。

        Returns:
            Any: 转换后的数据。
        """
        return data
