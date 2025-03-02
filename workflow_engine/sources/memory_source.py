from typing import Any, Optional, AsyncIterator
from workflow_engine.core.source import Source
from workflow_engine.interfaces.source_interface import StreamMode


class MemorySource(Source):
    """内存数据源,支持从内存中的数据结构读取数据"""

    def __init__(self, data: Any, mode: StreamMode = 'r'):
        super().__init__(str(data), mode)
        self._data = data
        self._position = 0

    async def open(self, mode: StreamMode = 'r') -> None:
        """打开内存数据源"""
        if 'r' not in mode:
            raise ValueError(f"Unsupported mode: {mode}")
        self._position = 0

    async def close(self) -> None:
        """关闭内存数据源"""
        self._position = 0

    async def read(self, n: int = -1) -> Any:
        """读取内存数据"""
        if n == -1:
            data = self._data[self._position:]
            self._position = len(self._data)
        else:
            end = min(self._position + n, len(self._data))
            data = self._data[self._position:end]
            self._position = end
        return data

    async def readline(self) -> Any:
        """读取一行内存数据"""
        if isinstance(self._data, str):
            newline_pos = self._data.find('\n', self._position)
            if newline_pos == -1:
                data = self._data[self._position:]
                self._position = len(self._data)
            else:
                data = self._data[self._position:newline_pos + 1]
                self._position = newline_pos + 1
            return data
        else:
            raise RuntimeError("readline() only supports string data")

    async def readlines(self) -> AsyncIterator[Any]:
        """逐行读取内存数据"""
        if isinstance(self._data, str):
            start = self._position
            while True:
                newline_pos = self._data.find('\n', start)
                if newline_pos == -1:
                    if start < len(self._data):
                        yield self._data[start:]
                    break
                else:
                    yield self._data[start:newline_pos + 1]
                    start = newline_pos + 1
            self._position = len(self._data)
        else:
            raise RuntimeError("readlines() only supports string data")

    async def write(self, data: Any) -> None:
        """写入内存数据(不支持)"""
        raise NotImplementedError("MemorySource does not support write operation")

    async def writelines(self, lines: AsyncIterator[Any]) -> None:
        """逐行写入内存数据(不支持)"""
        raise NotImplementedError("MemorySource does not support write operation")

    def get_size(self) -> Optional[int]:
        """获取数据大小"""
        try:
            return len(self._data)
        except TypeError:
            return None

    def is_seekable(self) -> bool:
        """判断是否可随机访问"""
        return True

    def seek(self, offset: int, whence: int = 0) -> None:
        """移动读写指针"""
        if whence == 0:
            self._position = offset
        elif whence == 1:
            self._position += offset
        elif whence == 2:
            self._position = len(self._data) + offset
        else:
            raise ValueError(f"Invalid whence value: {whence}")

        if self._position < 0:
            self._position = 0
        elif self._position > len(self._data):
            self._position = len(self._data)

    def tell(self) -> int:
        """获取当前读写指针位置"""
        return self._position 