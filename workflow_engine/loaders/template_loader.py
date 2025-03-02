from typing import Any
from workflow_engine.interfaces.loader_interface import LoaderInterface
from workflow_engine.core.source import Source

class TemplateLoader(LoaderInterface):
    """
    模板加载器。
    
    用于加载模板文件（如 Jinja2、Mako 等），并将其解析为可渲染的模板对象。
    """

    def __init__(self):
        self.type = 'template'
        self.options = {}

    def load(self, path: str) -> Source:
        """
        加载指定路径的模板文件。

        Args:
            path (str): 模板文件路径。

        Returns:
            Source: 加载后的模板源对象。
        """
        if not path.endswith(('.jinja2', '.mako', '.html')):
            raise ValueError(f"Unsupported template format: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        return Source(path, 'template', template_content)

    def is_supported(self, path: str) -> bool:
        """
        判断是否支持加载指定路径的模板文件。

        Args:
            path (str): 文件路径。

        Returns:
            bool: 如果支持，返回 True；否则返回 False。
        """
        return path.endswith(('.jinja2', '.mako', '.html'))

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。

        Args:
            data (Any): 加载后的数据。

        Returns:
            Any: 转换后的数据。
        """
        return data
