from workflow.interfaces.loader_interface import LoaderInterface
from workflow.core.source import Source

class ImageLoader(LoaderInterface):
    """
    图片加载器。
    
    用于加载图片文件。
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