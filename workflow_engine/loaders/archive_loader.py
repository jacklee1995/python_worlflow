import zipfile
import tarfile
from typing import Any, List
from workflow_engine.interfaces.loader_interface import LoaderInterface
from workflow_engine.core.source import Source

class ArchiveLoader(LoaderInterface):
    """
    压缩文件加载器。
    
    用于加载压缩文件（如 ZIP、TAR 等），并将其解压为文件列表。
    """

    def __init__(self):
        self.type = 'archive'
        self.options = {}

    def load(self, path: str) -> List[Source]:
        """
        加载指定路径的压缩文件并解压为文件列表。

        Args:
            path (str): 压缩文件路径。

        Returns:
            List[Source]: 解压后的文件列表。
        """
        if path.endswith('.zip'):
            with zipfile.ZipFile(path, 'r') as zip_ref:
                return [Source(name, 'file') for name in zip_ref.namelist()]
        elif path.endswith('.tar') or path.endswith('.tar.gz') or path.endswith('.tar.bz2'):
            with tarfile.open(path, 'r:*') as tar_ref:
                return [Source(name, 'file') for name in tar_ref.getnames()]
        else:
            raise ValueError(f"Unsupported archive format: {path}")

    def is_supported(self, path: str) -> bool:
        """
        判断是否支持加载指定路径的压缩文件。

        Args:
            path (str): 文件路径。

        Returns:
            bool: 如果支持，返回 True；否则返回 False。
        """
        return path.endswith(('.zip', '.tar', '.tar.gz', '.tar.bz2'))

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。

        Args:
            data (Any): 加载后的数据。

        Returns:
            Any: 转换后的数据。
        """
        return data
