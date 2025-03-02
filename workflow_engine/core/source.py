from typing import Any, List, Callable, Optional, AsyncIterator, Dict
import os
import requests
import asyncio
from asyncio import StreamReader, StreamWriter
from urllib.parse import urlparse

from workflow_engine.interfaces.loader_interface import LoaderInterface
from workflow_engine.interfaces.source_interface import SourceInterface, StreamMode
from workflow_engine.interfaces.step_interface import StepInterface


class Source(SourceInterface):
    """基于 asyncio 实现的数据源"""

    def __init__(self, uri: str, mode: StreamMode = 'r'):
        self.uri = uri
        self.mode = mode
        self._reader: Optional[StreamReader] = None
        self._writer: Optional[StreamWriter] = None
        self._transport: Optional[asyncio.BaseTransport] = None
        self._buffer_size = 64 * 1024  # 64KB
        self._closing = False
        self._closed = False
        self._exception: Optional[Exception] = None
        self._event_handlers: Dict[str, list[Callable]] = {
            'data': [],
            'end': [], 
            'error': [],
            'close': [],
            'drain': [],
            'pipe': [],
            'unpipe': []
        }
        self._paused = False
        self._eof_received = False

    async def open(self, mode: StreamMode = 'r') -> None:
        parsed = urlparse(self.uri)
        
        if parsed.scheme in ('file', ''):
            # 文件源
            path = parsed.path or parsed.netloc
            if 'r' in self.mode:  # 包含读取权限
                self._reader = StreamReader()
                with open(path, 'rb') as f:
                    self._reader.feed_data(f.read())
                    self._reader.feed_eof()
            
            if 'w' in self.mode or 'a' in self.mode:  # 包含写入权限
                # 创建文件写入器
                loop = asyncio.get_event_loop()
                transport, protocol = await loop.connect_write_pipe(
                    asyncio.streams.FlowControlMixin,
                    os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT))
                )
                self._writer = StreamWriter(transport, protocol, None, loop)
                
        elif parsed.scheme in ('http', 'https'):
            # HTTP(S)源
            reader, writer = await asyncio.open_connection(
                parsed.hostname,
                parsed.port or (443 if parsed.scheme == 'https' else 80)
            )
            self._reader = reader
            self._writer = writer
            
        elif parsed.scheme == 'tcp':
            # TCP源
            reader, writer = await asyncio.open_connection(
                parsed.hostname,
                parsed.port
            )
            self._reader = reader
            self._writer = writer
            
        else:
            raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    async def get_reader(self) -> StreamReader:
        if not self._reader:
            raise RuntimeError("Source not opened or not readable")
        return self._reader

    async def get_writer(self) -> Optional[StreamWriter]:
        return self._writer

    async def read(self, n: int = -1) -> bytes:
        if not self._reader:
            raise RuntimeError("Source not opened or not readable")
        data = await self._reader.read(n)
        if data:
            for handler in self._event_handlers['data']:
                handler(data)
        return data

    async def readline(self) -> bytes:
        if not self._reader:
            raise RuntimeError("Source not opened or not readable")
        return await self._reader.readline()

    async def readexactly(self, n: int) -> bytes:
        if not self._reader:
            raise RuntimeError("Source not opened or not readable")
        return await self._reader.readexactly(n)

    async def readuntil(self, separator: bytes = b'\n') -> bytes:
        if not self._reader:
            raise RuntimeError("Source not opened or not readable")
        return await self._reader.readuntil(separator)

    async def write(self, data: bytes) -> None:
        if not self._writer:
            raise RuntimeError("Source not opened or not writable")
        self._writer.write(data)
        await self._writer.drain()

    async def drain(self) -> None:
        if not self._writer:
            raise RuntimeError("Source not opened or not writable")
        await self._writer.drain()
        for handler in self._event_handlers['drain']:
            handler()

    async def write_eof(self) -> None:
        if not self._writer:
            raise RuntimeError("Source not opened or not writable")
        self._writer.write_eof()
        await self._writer.drain()
        self._eof_received = True
        for handler in self._event_handlers['end']:
            handler()

    async def close(self) -> None:
        if self._writer:
            self._writer.close()
            await self._writer.wait_closed()
        self._closed = True
        for handler in self._event_handlers['close']:
            handler()

    async def wait_closed(self) -> None:
        if self._writer:
            await self._writer.wait_closed()

    def is_closing(self) -> bool:
        return self._closing

    async def pipe(self, destination: 'SourceInterface') -> None:
        for handler in self._event_handlers['pipe']:
            handler(destination)
            
        async for chunk in self:
            transformed = await self.transform(chunk)
            destination.write(transformed)
            await destination.drain()

        destination.write_eof()
        
        for handler in self._event_handlers['unpipe']:
            handler(destination)

    async def transform(self, chunk: bytes) -> bytes:
        return chunk

    async def __aiter__(self) -> AsyncIterator[bytes]:
        while True:
            chunk = await self.read(self._buffer_size)
            if not chunk:
                break
            yield chunk

    def at_eof(self) -> bool:
        return self._eof_received

    def exception(self) -> Optional[Exception]:
        return self._exception

    def set_exception(self, exc: Exception) -> None:
        self._exception = exc
        for handler in self._event_handlers['error']:
            handler(exc)

    def feed_data(self, data: bytes) -> None:
        if self._reader:
            self._reader.feed_data(data)
            for handler in self._event_handlers['data']:
                handler(data)

    def feed_eof(self) -> None:
        if self._reader:
            self._reader.feed_eof()
            self._eof_received = True
            for handler in self._event_handlers['end']:
                handler()

    def set_transport(self, transport: asyncio.BaseTransport) -> None:
        self._transport = transport

    def get_transport(self) -> Optional[asyncio.BaseTransport]:
        return self._transport

    def pause_reading(self) -> None:
        self._paused = True
        if self._transport:
            self._transport.pause_reading()

    def resume_reading(self) -> None:
        self._paused = False
        if self._transport:
            self._transport.resume_reading()

    def on(self, event: str, callback: Callable) -> None:
        if event not in self._event_handlers:
            raise ValueError(f"Unsupported event: {event}")
        self._event_handlers[event].append(callback)

    def off(self, event: str, callback: Optional[Callable] = None) -> None:
        if event not in self._event_handlers:
            raise ValueError(f"Unsupported event: {event}")
        if callback is None:
            self._event_handlers[event].clear()
        else:
            self._event_handlers[event] = [
                h for h in self._event_handlers[event] if h != callback
            ]

    def readable(self) -> bool:
        return bool(self._reader) and not self._paused

    def writable(self) -> bool:
        return bool(self._writer) and not self._closing

    def closed(self) -> bool:
        return self._closed

    def get_buffer_size(self) -> int:
        return self._buffer_size

    def set_buffer_size(self, size: int) -> None:
        self._buffer_size = size

    def read(self) -> Optional[Any]:
        raise NotImplementedError("Subclasses must implement the 'read' method.")

    def write(self, data: Any) -> None:
        raise NotImplementedError("Subclasses must implement the 'write' method.")

    def pipe(self, step: StepInterface) -> SourceInterface:
        return step.process(self)

    def on_error(self, error_handler: Callable[[Exception], None]) -> None:
        self._error_handler = error_handler

    def on_complete(self, complete_handler: Callable[[], None]) -> None:
        self._complete_handler = complete_handler

    def is_readable(self) -> bool:
        return 'r' in self.mode

    def is_writable(self) -> bool:
        return 'w' in self.mode or 'a' in self.mode

    def close(self) -> None:
        pass

    def get_metadata(self) -> dict:
        return self._metadata.copy()

    def set_metadata(self, metadata: dict) -> None:
        self._metadata.update(metadata)

    def get_position(self) -> Optional[Any]:
        return self._position

    def set_position(self, position: Any) -> None:
        self._position = position

    def rewind(self) -> None:
        self._position = 0

    def get_size(self) -> Optional[int]:
        return None

    def is_seekable(self) -> bool:
        return False

    def _handle_error(self, exception: Exception) -> None:
        if self._error_handler:
            self._error_handler(exception)
        else:
            raise exception

    def _handle_complete(self) -> None:
        if self._complete_handler:
            self._complete_handler()

    def load(self, loader: 'LoaderInterface') -> None:
        """
        使用指定的加载器加载数据源。

        Args:
            loader (LoaderInterface): 加载器对象。
        """
        self._data = loader.load(self.path)

    def get_data(self) -> Any:
        """
        获取数据源的数据。

        Returns:
            Any: 数据源的数据。
        """
        return self._data

    def set_data(self, data: Any) -> None:
        """
        设置数据源的数据。

        Args:
            data (Any): 要设置的数据。
        """
        self._data = data

    def get_path(self) -> str:
        """
        获取数据源的路径。

        Returns:
            str: 数据源的路径。
        """
        return self.path

    def set_path(self, path: str) -> None:
        """
        设置数据源的路径。

        Args:
            path (str): 数据源的路径。
        """
        self.path = path

    def get_name(self) -> str:
        """
        获取数据源的名称。

        Returns:
            str: 数据源的名称。
        """
        return os.path.basename(self.path)

    def set_name(self, name: str) -> None:
        """
        设置数据源的名称。

        Args:
            name (str): 数据源的名称。
        """
        base, ext = os.path.splitext(self.path)
        self.path = os.path.join(os.path.dirname(self.path), f"{name}{ext}")

    def get_type(self) -> str:
        """
        获取数据源的类型。

        Returns:
            str: 数据源的类型。
        """
        return self.type

    def set_type(self, type: str) -> None:
        """
        设置数据源的类型。

        Args:
            type (str): 数据源的类型。
        """
        self.type = type

    def exists(self) -> bool:
        """
        检查数据源是否存在。

        Returns:
            bool: 如果数据源存在，则返回 True，否则返回 False。
        """
        if self.type == 'url':
            try:
                response = requests.head(self.path)
                return response.status_code == 200
            except requests.exceptions.RequestException:
                return False
        return os.path.exists(self.path)

    def is_file(self) -> bool:
        """
        检查数据源是否为文件。

        Returns:
            bool: 如果数据源是文件，则返回 True，否则返回 False。
        """
        return self.type == 'file' and os.path.isfile(self.path)

    def is_dir(self) -> bool:
        """
        检查数据源是否为目录。

        Returns:
            bool: 如果数据源是目录，则返回 True，否则返回 False。
        """
        return self.type == 'dir' and os.path.isdir(self.path)

    def is_url(self) -> bool:
        """
        检查数据源是否为 URL。

        Returns:
            bool: 如果数据源是 URL，则返回 True，否则返回 False。
        """
        return self.type == 'url'

    def get_files(self, pattern: str = None) -> List['SourceInterface']:
        """
        获取数据源中符合指定模式的文件。

        Args:
            pattern (str): 文件模式，可以包含通配符。默认为 None，表示获取所有文件。

        Returns:
            List[SourceInterface]: 符合指定模式的文件列表。
        """
        if not self.is_dir():
            return []
        files = []
        for entry in os.listdir(self.path):
            entry_path = os.path.join(self.path, entry)
            if os.path.isfile(entry_path) and (not pattern or entry.endswith(pattern)):
                files.append(Source(entry_path, 'file'))
        return files

    def get_dirs(self, pattern: str = None) -> List['SourceInterface']:
        """
        获取数据源中符合指定模式的目录。

        Args:
            pattern (str): 目录模式，可以包含通配符。默认为 None，表示获取所有目录。

        Returns:
            List[SourceInterface]: 符合指定模式的目录列表。
        """
        if not self.is_dir():
            return []
        dirs = []
        for entry in os.listdir(self.path):
            entry_path = os.path.join(self.path, entry)
            if os.path.isdir(entry_path) and (not pattern or entry.endswith(pattern)):
                dirs.append(Source(entry_path, 'dir'))
        return dirs

    def get_urls(self, pattern: str = None) -> List['SourceInterface']:
        """
        获取数据源中符合指定模式的 URL。

        Args:
            pattern (str): URL 模式，可以包含通配符。默认为 None，表示获取所有 URL。

        Returns:
            List[SourceInterface]: 符合指定模式的 URL 列表。
        """
        if not self.is_url():
            return []
        return [self] if not pattern or self.path.endswith(pattern) else []

    def get_all(self, pattern: str = None) -> List['SourceInterface']:
        """
        获取数据源中符合指定模式的所有文件、目录和 URL。

        Args:
            pattern (str): 文件、目录和 URL 模式，可以包含通配符。默认为 None，表示获取所有。

        Returns:
            List[SourceInterface]: 符合指定模式的文件、目录和 URL 列表。
        """
        if self.is_file():
            return [self] if not pattern or self.path.endswith(pattern) else []
        elif self.is_dir():
            return self.get_files(pattern) + self.get_dirs(pattern)
        elif self.is_url():
            return self.get_urls(pattern)
        return []


