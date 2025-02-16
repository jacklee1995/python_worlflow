from typing import Any
from workflow.interfaces.loader_interface import LoaderInterface
from workflow.core.source import Source

class HtmlLoader(LoaderInterface):
    """
    HTML 加载器。
    
    用于加载 HTML 文件，并将其作为字符串或解析后的 DOM 对象返回。
    """

    def __init__(self):
        self.type = 'html'
        self.options = {}

    def load(self, path: str) -> Source:
        """
        加载指定路径的 HTML 文件。

        Args:
            path (str): HTML 文件路径。

        Returns:
            Source: 加载后的 HTML 源对象。
        """
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        return Source(path, 'html', html)

    def is_supported(self, path: str) -> bool:
        """
        判断是否支持加载指定路径的 HTML 文件。

        Args:
            path (str): 文件路径。

        Returns:
            bool: 如果支持，返回 True；否则返回 False。
        """
        return path.endswith('.html') or path.endswith('.htm')

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。

        Args:
            data (Any): 加载后的数据。

        Returns:
            Any: 转换后的数据。
        """
        return data
