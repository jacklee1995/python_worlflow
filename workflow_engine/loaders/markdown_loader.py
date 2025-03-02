import markdown
from typing import Any
from workflow_engine.interfaces.loader_interface import LoaderInterface
from workflow_engine.core.source import Source

class MarkdownLoader(LoaderInterface):
    """
    Markdown 加载器。
    
    用于加载 Markdown 文件，并将其解析为 HTML 或纯文本。
    """

    def __init__(self):
        self.type = 'markdown'
        self.options = {}

    def load(self, path: str) -> Source:
        """
        加载指定路径的 Markdown 文件。
        """
        if not path.endswith(('.md', '.markdown')):
            raise ValueError(f"Unsupported markdown format: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        html = markdown.markdown(markdown_content)
        return Source(path, 'markdown', html)

    def is_supported(self, path: str) -> bool:
        """
        判断是否支持加载指定路径的 Markdown 文件。
        """
        return path.endswith(('.md', '.markdown'))

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。
        """
        return data
