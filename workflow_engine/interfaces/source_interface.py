from abc import ABC, abstractmethod
from typing import Callable, Optional, AsyncIterator, Literal
import asyncio
from asyncio import StreamReader, StreamWriter

# 使用 Literal 类型来定义合法的模式字符串
StreamMode = Literal['r', 'w', 'a', 'r+', 'w+', 'a+', 'rb', 'wb', 'ab', 'r+b', 'w+b', 'a+b']

class SourceInterface(ABC):
    """
    数据源接口，实现严格意义上的流（Stream）。
    支持异步迭代、事件驱动和双向数据流。
    """

    @abstractmethod
    async def open(self, mode: StreamMode = 'r') -> None:
        """
        打开数据源
        
        Args:
            mode: 打开模式，支持标准 Python 文件模式:
                'r'  - 只读（默认）
                'w'  - 只写
                'a'  - 追加
                'r+' - 读写
                'w+' - 读写，覆盖已存在文件
                'a+' - 读写，追加模式
                还可以添加 'b' 后缀表示二进制模式
        """
        pass

    @abstractmethod
    async def get_reader(self) -> StreamReader:
        """获取底层的 StreamReader"""
        pass

    @abstractmethod
    async def get_writer(self) -> Optional[StreamWriter]:
        """获取底层的 StreamWriter"""
        pass

    @abstractmethod
    async def read(self, n: int = -1) -> bytes:
        """读取数据"""
        pass

    @abstractmethod
    async def readline(self) -> bytes:
        """读取一行数据"""
        pass

    @abstractmethod
    async def readexactly(self, n: int) -> bytes:
        """精确读取指定字节数的数据"""
        pass

    @abstractmethod
    async def readuntil(self, separator: bytes = b'\n') -> bytes:
        """读取直到分隔符"""
        pass

    @abstractmethod
    def write(self, data: bytes) -> None:
        """写入数据"""
        pass

    @abstractmethod
    async def drain(self) -> None:
        """等待写入缓冲区清空"""
        pass

    @abstractmethod
    def write_eof(self) -> None:
        """写入EOF标记"""
        pass

    @abstractmethod
    def close(self) -> None:
        """关闭数据源"""
        pass

    @abstractmethod
    async def wait_closed(self) -> None:
        """等待数据源完全关闭"""
        pass

    @abstractmethod
    def is_closing(self) -> bool:
        """检查是否正在关闭"""
        pass

    @abstractmethod
    async def pipe(self, destination: 'SourceInterface') -> None:
        """将数据管道传输到另一个数据源"""
        pass

    @abstractmethod
    async def transform(self, chunk: bytes) -> bytes:
        """转换数据块"""
        pass

    @abstractmethod
    async def __aiter__(self) -> AsyncIterator[bytes]:
        """支持异步迭代"""
        pass

    @abstractmethod
    def at_eof(self) -> bool:
        """检查是否到达EOF"""
        pass

    @abstractmethod
    def exception(self) -> Optional[Exception]:
        """获取异常信息"""
        pass

    @abstractmethod
    def set_exception(self, exc: Exception) -> None:
        """设置异常"""
        pass

    @abstractmethod
    def feed_data(self, data: bytes) -> None:
        """输入数据到流"""
        pass

    @abstractmethod
    def feed_eof(self) -> None:
        """输入EOF标记"""
        pass

    @abstractmethod
    def set_transport(self, transport: asyncio.BaseTransport) -> None:
        """设置传输层"""
        pass

    @abstractmethod
    def get_transport(self) -> Optional[asyncio.BaseTransport]:
        """获取传输层"""
        pass

    @abstractmethod
    def pause_reading(self) -> None:
        """暂停读取"""
        pass

    @abstractmethod
    def resume_reading(self) -> None:
        """恢复读取"""
        pass

    @abstractmethod
    def on(self, event: str, callback: Callable) -> None:
        """
        注册事件处理器。

        Args:
            event (str): 事件名称，可以是：
                        'data': 有新数据可读
                        'end': 数据读取结束
                        'error': 发生错误
                        'close': 流关闭
                        'drain': 写入缓冲区已空
                        'pipe': 流被管道传输
                        'unpipe': 流取消管道传输
            callback (Callable): 事件处理函数。
        """
        pass

    @abstractmethod
    def off(self, event: str, callback: Optional[Callable] = None) -> None:
        """
        移除事件处理器。

        Args:
            event (str): 事件名称。
            callback (Optional[Callable]): 要移除的处理函数，
                                         如果为 None 则移除该事件的所有处理器。
        """
        pass

    @abstractmethod
    def readable(self) -> bool:
        """
        检查流是否可读。

        Returns:
            bool: 如果流可读返回 True。
        """
        pass

    @abstractmethod
    def writable(self) -> bool:
        """
        检查流是否可写。

        Returns:
            bool: 如果流可写返回 True。
        """
        pass

    @abstractmethod
    def closed(self) -> bool:
        """
        检查流是否已关闭。

        Returns:
            bool: 如果流已关闭返回 True。
        """
        pass

    @abstractmethod
    def get_buffer_size(self) -> int:
        """
        获取缓冲区大小。

        Returns:
            int: 缓冲区当前大小（字节）。
        """
        pass

    @abstractmethod
    def set_buffer_size(self, size: int) -> None:
        """
        设置缓冲区大小。

        Args:
            size (int): 新的缓冲区大小（字节）。
        """
        pass