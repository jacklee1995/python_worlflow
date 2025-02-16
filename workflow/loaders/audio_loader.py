from typing import Any
from workflow.interfaces.loader_interface import LoaderInterface
from workflow.core.source import Source

class AudioLoader(LoaderInterface):
    """
    音频加载器。
    
    用于加载音频文件（如 MP3、WAV 等），并将其作为资源对象返回。
    """

    def __init__(self):
        self.type = 'audio'
        self.options = {}

    def load(self, path: str) -> Source:
        """
        加载指定路径的音频文件。

        Args:
            path (str): 音频文件路径。

        Returns:
            Source: 加载后的音频源对象。
        """
        if not path.endswith(('.mp3', '.wav', '.ogg', '.flac')):
            raise ValueError(f"Unsupported audio format: {path}")
        return Source(path, 'audio')

    def is_supported(self, path: str) -> bool:
        """
        判断是否支持加载指定路径的音频文件。

        Args:
            path (str): 文件路径。

        Returns:
            bool: 如果支持，返回 True；否则返回 False。
        """
        return path.endswith(('.mp3', '.wav', '.ogg', '.flac'))

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。

        Args:
            data (Any): 加载后的数据。

        Returns:
            Any: 转换后的数据。
        """
        return data
