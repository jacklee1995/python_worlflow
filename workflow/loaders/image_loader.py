from typing import Any
from workflow.interfaces.loader_interface import LoaderInterface
from workflow.core.source import Source

class ImageLoader(LoaderInterface):
    """
    图片加载器。
    
    用于加载图片文件（如 PNG、JPG、GIF 等），并将其作为资源对象返回。
    """

    def __init__(self):
        self.type = 'image'
        self.options = {}

    def load(self, path: str) -> Source:
        """
        加载指定路径的图片文件。
        """
        if not path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            raise ValueError(f"Unsupported image format: {path}")
        return Source(path, 'image')

    def is_supported(self, path: str) -> bool:
        """
        判断是否支持加载指定路径的图片文件。
        """
        return path.endswith(('.png', '.jpg', '.jpeg', '.gif'))

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。
        """
        return data 