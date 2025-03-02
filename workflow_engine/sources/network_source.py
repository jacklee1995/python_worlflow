import aiohttp
from typing import Optional, AsyncIterator
from workflow_engine.core.source import Source
from workflow_engine.interfaces.source_interface import StreamMode


class NetworkSource(Source):
    """网络数据源,支持通过 HTTP/HTTPS 读取远程数据"""

    def __init__(self, url: str, mode: StreamMode = 'r'):
        super().__init__(url, mode)
        self._url = url
        self._session = None
        self._response = None

    async def open(self, mode: StreamMode = 'r') -> None:
        """打开网络连接"""
        if 'r' not in mode:
            raise ValueError(f"Unsupported mode: {mode}")
        self._session = aiohttp.ClientSession()
        self._response = await self._session.get(self._url)
        self._response.raise_for_status()

    async def close(self) -> None:
        """关闭网络连接"""
        if self._response:
            await self._response.release()
            self._response = None
        if self._session:
            await self._session.close()
            self._session = None

    async def read(self, n: int = -1) -> bytes:
        """读取网络数据"""
        if not self._response:
            raise RuntimeError("Connection not opened")
        return await self._response.content.read(n)

    async def readline(self) -> bytes:
        """读取一行网络数据"""
        if not self._response:
            raise RuntimeError("Connection not opened")
        return await self._response.content.readline()

    async def readlines(self) -> AsyncIterator[bytes]:
        """逐行读取网络数据"""
        if not self._response:
            raise RuntimeError("Connection not opened")
        async for line in self._response.content:
            yield line

    async def write(self, data: bytes) -> None:
        """写入网络数据(不支持)"""
        raise NotImplementedError("NetworkSource does not support write operation")

    async def writelines(self, lines: AsyncIterator[bytes]) -> None:
        """逐行写入网络数据(不支持)"""
        raise NotImplementedError("NetworkSource does not support write operation")

    def get_size(self) -> Optional[int]:
        """获取数据大小"""
        if not self._response:
            return None
        return self._response.content_length

    def is_seekable(self) -> bool:
        """判断是否可随机访问"""
        return False

    def seek(self, offset: int, whence: int = 0) -> None:
        """移动读写指针(不支持)"""
        raise NotImplementedError("NetworkSource does not support seek operation")

    def tell(self) -> int:
        """获取当前读写指针位置(不支持)"""
        raise NotImplementedError("NetworkSource does not support tell operation") 