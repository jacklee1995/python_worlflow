from typing import Any
from workflow.interfaces.loader_interface import LoaderInterface
from workflow.core.source import Source

class FontLoader(LoaderInterface):
    """
    字体加载器。
    
    用于加载字体文件（如 TTF、OTF、WOFF 等），并将其作为资源对象返回。
    """

    def __init__(self):
        self.type = 'font'
        self.options = {}

    def load(self, path: str) -> Source:
        """
        加载指定路径的字体文件。

        Args:
            path (str): 字体文件路径。

        Returns:
            Source: 加载后的字体源对象。
        """
        if not path.endswith(('.ttf', '.otf', '.woff', '.woff2')):
            raise ValueError(f"Unsupported font format: {path}")
        return Source(path, 'font')

    def is_supported(self, path: str) -> bool:
        """
        判断是否支持加载指定路径的字体文件。

        Args:
            path (str): 文件路径。

        Returns:
            bool: 如果支持，返回 True；否则返回 False。
        """
        return path.endswith(('.ttf', '.otf', '.woff', '.woff2'))

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。

        Args:
            data (Any): 加载后的数据。

        Returns:
            Any: 转换后的数据。
        """
        return data
