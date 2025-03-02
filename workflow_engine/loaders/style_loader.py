from typing import Any
from workflow_engine.interfaces.loader_interface import LoaderInterface
from workflow_engine.core.source import Source

class StyleLoader(LoaderInterface):
    """
    样式加载器。
    
    用于加载 CSS 或 SCSS 文件，并将其解析为 CSS 字符串。
    """

    def __init__(self):
        self.type = 'style'
        self.options = {}

    def load(self, path: str) -> Source:
        """
        加载指定路径的样式文件。
        """
        if not path.endswith(('.css', '.scss')):
            raise ValueError(f"Unsupported style format: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            style = f.read()
        return Source(path, 'style', style)

    def is_supported(self, path: str) -> bool:
        """
        判断是否支持加载指定路径的样式文件。
        """
        return path.endswith(('.css', '.scss'))

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。
        """
        return data
