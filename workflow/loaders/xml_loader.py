import xml.etree.ElementTree as ET
from typing import Any
from workflow.interfaces.loader_interface import LoaderInterface
from workflow.core.source import Source

class XmlLoader(LoaderInterface):
    """
    XML 加载器。
    
    用于加载 XML 文件，并将其解析为 Python 的 ElementTree 对象。
    """

    def __init__(self):
        self.type = 'xml'
        self.options = {}

    def load(self, path: str) -> Any:
        """
        加载指定路径的 XML 文件并解析为 ElementTree 对象。

        Args:
            path (str): XML 文件路径。

        Returns:
            Any: 解析后的 ElementTree 对象。
        """
        if not path.endswith('.xml'):
            raise ValueError(f"Unsupported file format: {path}")
        return ET.parse(path)

    def is_supported(self, path: str) -> bool:
        """
        判断是否支持加载指定路径的 XML 文件。

        Args:
            path (str): 文件路径。

        Returns:
            bool: 如果支持，返回 True；否则返回 False。
        """
        return path.endswith('.xml')

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。

        Args:
            data (Any): 加载后的数据。

        Returns:
            Any: 转换后的数据。
        """
        return data
