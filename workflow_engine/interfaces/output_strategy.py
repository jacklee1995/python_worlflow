from abc import ABC, abstractmethod
from typing import Any, Optional, Callable, List, Dict, AsyncIterator
import asyncio
from asyncio import StreamWriter

from .output_types import OutputErrorType, RetryPolicy, OutputMetrics


class OutputStrategy(ABC):
    """输出策略接口，定义基于流的异步输出行为"""

    @abstractmethod
    async def open(self) -> None:
        """打开输出目标"""
        pass

    @abstractmethod
    async def get_writer(self) -> StreamWriter:
        """获取底层的 StreamWriter"""
        pass

    @abstractmethod
    async def write(self, data: bytes) -> None:
        """异步写入数据"""
        pass

    @abstractmethod
    async def write_batch(self, data: List[bytes], chunk_size: int = 8192) -> None:
        """批量写入数据"""
        pass

    @abstractmethod
    async def drain(self) -> None:
        """等待写入缓冲区清空"""
        pass

    @abstractmethod
    async def flush(self) -> None:
        """强制刷新缓冲数据"""
        pass

    @abstractmethod
    async def write_eof(self) -> None:
        """写入EOF标记"""
        pass

    @abstractmethod
    async def close(self) -> None:
        """关闭输出目标"""
        pass

    @abstractmethod
    async def wait_closed(self) -> None:
        """等待输出目标完全关闭"""
        pass

    @abstractmethod
    def is_closing(self) -> bool:
        """检查是否正在关闭"""
        pass

    @abstractmethod
    def writable(self) -> bool:
        """检查输出是否可写"""
        pass

    @abstractmethod
    def closed(self) -> bool:
        """检查输出是否已关闭"""
        pass

    @abstractmethod
    def get_buffer_size(self) -> int:
        """获取缓冲区大小"""
        pass

    @abstractmethod
    def set_buffer_size(self, size: int) -> None:
        """设置缓冲区大小"""
        pass

    @abstractmethod
    def get_metrics(self) -> OutputMetrics:
        """获取性能指标"""
        pass

    @abstractmethod
    def reset_metrics(self) -> None:
        """重置性能指标"""
        pass

    @abstractmethod
    def set_retry_policy(self, policy: RetryPolicy) -> None:
        """设置重试策略"""
        pass

    @abstractmethod
    def get_retry_policy(self) -> RetryPolicy:
        """获取重试策略"""
        pass

    @abstractmethod
    def enable_buffering(self) -> None:
        """启用缓冲"""
        pass

    @abstractmethod
    def disable_buffering(self) -> None:
        """禁用缓冲"""
        pass

    @abstractmethod
    def get_buffer_usage(self) -> float:
        """获取缓冲区使用率"""
        pass

    @abstractmethod
    def on(self, event: str, callback: Callable) -> None:
        """注册事件处理器"""
        pass

    @abstractmethod
    def off(self, event: str, callback: Optional[Callable] = None) -> None:
        """移除事件处理器"""
        pass

    @abstractmethod
    async def chain(self, next_strategy: 'OutputStrategy') -> None:
        """链接到下一个输出策略"""
        pass

    @abstractmethod
    async def unchain(self, strategy: 'OutputStrategy') -> None:
        """解除与指定策略的链接"""
        pass

    @abstractmethod
    def get_chained_strategies(self) -> List['OutputStrategy']:
        """获取所有链接的策略"""
        pass

    @abstractmethod
    async def handle_error(self, error: Exception) -> None:
        """处理错误"""
        pass

    @abstractmethod
    def get_error_stats(self) -> Dict[OutputErrorType, int]:
        """获取错误统计"""
        pass

    @abstractmethod
    def clear_error_stats(self) -> None:
        """清除错误统计"""
        pass

    @abstractmethod
    async def read_chunks(self, chunk_size: int = 8192) -> AsyncIterator[bytes]:
        """读取数据块"""
        pass


class ConsoleOutputStrategy(OutputStrategy):
    """控制台输出策略"""

    def __init__(self):
        self._writer: Optional[StreamWriter] = None
        self._buffer_size = 64 * 1024  # 64KB
        self._closing = False
        self._closed = False
        self._event_handlers = {
            'data': [],
            'drain': [],
            'error': [],
            'close': [],
        }

    async def open(self) -> None:
        loop = asyncio.get_event_loop()
        transport, protocol = await loop.connect_write_pipe(
            asyncio.streams.FlowControlMixin,
            asyncio.streams.StreamWriter(asyncio.StreamWriter._std_out)
        )
        self._writer = StreamWriter(transport, protocol, None, loop)

    async def get_writer(self) -> StreamWriter:
        if not self._writer:
            await self.open()
        return self._writer

    async def write(self, data: bytes) -> None:
        writer = await self.get_writer()
        writer.write(data)
        for handler in self._event_handlers['data']:
            handler(data)

    async def drain(self) -> None:
        if self._writer:
            await self._writer.drain()
            for handler in self._event_handlers['drain']:
                handler()

    async def write_eof(self) -> None:
        if self._writer:
            self._writer.write_eof()

    async def close(self) -> None:
        if self._writer:
            self._writer.close()
            self._closing = True
            for handler in self._event_handlers['close']:
                handler()

    async def wait_closed(self) -> None:
        if self._writer:
            await self._writer.wait_closed()
            self._closed = True

    def is_closing(self) -> bool:
        return self._closing

    def writable(self) -> bool:
        return self._writer is not None and not self._closing

    def closed(self) -> bool:
        return self._closed

    def get_buffer_size(self) -> int:
        return self._buffer_size

    def set_buffer_size(self, size: int) -> None:
        self._buffer_size = size

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


class FileOutputStrategy(OutputStrategy):
    """
    文件输出策略，将数据输出到文件。
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file = None

    def write(self, data: Any) -> None:
        if self.file is None:
            self.file = open(self.file_path, 'w')
        self.file.write(str(data))

    def close(self) -> None:
        if self.file is not None:
            self.file.close()


class NetworkOutputStrategy(OutputStrategy):
    """
    网络输出策略，将数据输出到网络。
    """

    def __init__(self, url: str):
        self.url = url

    def write(self, data: Any) -> None:
        import requests
        requests.post(self.url, data=data)

    def close(self) -> None:
        pass 