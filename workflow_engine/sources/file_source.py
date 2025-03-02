import os
import yaml
from typing import Optional, AsyncIterator, Dict, Any
from workflow_engine.core.source import Source
from workflow_engine.interfaces.source_interface import StreamMode
from workflow_engine.core.config import Config


class FileSource(Source):
    """文件数据源,支持读取本地文件"""

    def __init__(self, file_path: str, mode: StreamMode = 'r', chunk_size: int = 4096):
        super().__init__(file_path, mode)
        self._file_path = file_path
        self._file = None
        self._chunk_size = chunk_size
        self._config: Optional[Config] = None
        self._load_config()

    def _load_config(self) -> None:
        """加载配置文件"""
        if self._file_path.endswith('.yaml') or self._file_path.endswith('.yml'):
            try:
                with open(self._file_path, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)
                self._config = Config(config_data)
            except Exception as e:
                print(f"Warning: Failed to load config from {self._file_path}: {e}")
                self._config = Config({})
        else:
            self._config = Config({})

    def get_config(self) -> Config:
        """获取配置对象"""
        return self._config

    def set_config(self, config: Config) -> None:
        """设置配置对象"""
        self._config = config

    async def open(self, mode: StreamMode = 'r') -> None:
        """打开文件"""
        if 'r' in mode:
            self._file = open(self._file_path, 'rb')
        elif 'w' in mode or 'a' in mode:
            self._file = open(self._file_path, 'wb' if 'b' in mode else 'w')
        else:
            raise ValueError(f"Unsupported mode: {mode}")

    async def close(self) -> None:
        """关闭文件"""
        if self._file:
            self._file.close()
            self._file = None

    async def read(self, n: int = -1) -> bytes:
        """读取文件数据"""
        if not self._file:
            raise RuntimeError("File not opened")
        return self._file.read(n)

    async def readline(self) -> bytes:
        """读取一行文件数据"""
        if not self._file:
            raise RuntimeError("File not opened")
        return self._file.readline()

    async def readlines(self) -> AsyncIterator[bytes]:
        """逐行读取文件数据"""
        if not self._file:
            raise RuntimeError("File not opened")
        for line in self._file:
            yield line

    async def read_chunks(self) -> AsyncIterator[bytes]:
        """分块读取文件数据"""
        if not self._file:
            raise RuntimeError("File not opened")
        while True:
            chunk = self._file.read(self._chunk_size)
            if not chunk:
                break
            yield chunk

    async def write(self, data: bytes) -> None:
        """写入文件数据"""
        if not self._file:
            raise RuntimeError("File not opened")
        self._file.write(data)

    async def writelines(self, lines: AsyncIterator[bytes]) -> None:
        """逐行写入文件数据"""
        if not self._file:
            raise RuntimeError("File not opened")
        for line in lines:
            self._file.write(line)

    def get_size(self) -> Optional[int]:
        """获取文件大小"""
        try:
            return os.path.getsize(self._file_path)
        except OSError:
            return None

    def is_seekable(self) -> bool:
        """判断文件是否可随机访问"""
        return True

    def seek(self, offset: int, whence: int = 0) -> None:
        """移动文件读写指针"""
        if not self._file:
            raise RuntimeError("File not opened")
        self._file.seek(offset, whence)

    def tell(self) -> int:
        """获取当前文件读写指针位置"""
        if not self._file:
            raise RuntimeError("File not opened")
        return self._file.tell() 