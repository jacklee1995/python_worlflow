from typing import Any
from workflow.interfaces.loader_interface import LoaderInterface
from workflow.core.source import Source

class VideoLoader(LoaderInterface):
    """
    视频加载器。
    
    用于加载视频文件（如 MP4、AVI 等），并将其作为资源对象返回。
    """

    def __init__(self):
        self.type = 'video'
        self.options = {}

    def load(self, path: str) -> Source:
        """
        加载指定路径的视频文件。
        """
        if not path.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            raise ValueError(f"Unsupported video format: {path}")
        return Source(path, 'video')

    def is_supported(self, path: str) -> bool:
        """
        判断是否支持加载指定路径的视频文件。
        """
        return path.endswith(('.mp4', '.avi', '.mov', '.mkv'))

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。
        """
        return data
