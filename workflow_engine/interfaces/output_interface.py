from abc import ABC, abstractmethod
from typing import Any, Optional, Callable, Dict, List, Union
from asyncio import StreamWriter

from .output_types import RetryPolicy, OutputMetrics
from .output_strategy import OutputStrategy


class OutputInterface(ABC):
    """
    输出接口，定义基于流的异步输出行为。
    """

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
        """批量写入数据，支持分块处理"""
        pass

    @abstractmethod
    async def drain(self) -> None:
        """等待写入缓冲区清空"""
        pass

    @abstractmethod
    async def flush(self) -> None:
        """强制刷新所有缓冲的数据到输出目标"""
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
    async def pipe(self, destination: 'OutputInterface', end: bool = True) -> None:
        """将输出管道传输到另一个输出目标"""
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
    def enable_event_handling(self) -> None:
        """启用事件处理"""
        pass

    @abstractmethod
    def disable_event_handling(self) -> None:
        """禁用事件处理"""
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
    def add_strategy(self, strategy: OutputStrategy) -> None:
        """添加输出策略"""
        pass

    @abstractmethod
    def remove_strategy(self, strategy: OutputStrategy) -> None:
        """移除输出策略"""
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
    def is_resource_leak(self) -> bool:
        """检查是否存在资源泄漏"""
        pass

    @abstractmethod
    async def __aenter__(self) -> 'OutputInterface':
        """异步上下文管理器入口"""
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """异步上下文管理器出口"""
        pass

    @abstractmethod
    async def write_text(self, text: str, encoding: str = 'utf-8') -> None:
        """写入文本数据"""
        pass

    @abstractmethod
    async def write_json(self, data: Any, indent: Optional[int] = None) -> None:
        """写入JSON数据"""
        pass

    @abstractmethod
    async def write_lines(self, lines: List[str], encoding: str = 'utf-8') -> None:
        """写入多行文本"""
        pass

    @abstractmethod
    def set_encoding(self, encoding: str) -> None:
        """设置文本编码"""
        pass

    @abstractmethod
    def get_encoding(self) -> str:
        """获取文本编码"""
        pass

    @abstractmethod
    def set_timeout(self, timeout: float) -> None:
        """设置操作超时时间"""
        pass

    @abstractmethod
    def get_timeout(self) -> float:
        """获取操作超时时间"""
        pass

    @abstractmethod
    def on(self, event: str, callback: Callable) -> None:
        """
        注册事件处理器。

        Args:
            event (str): 事件名称，可以是：
                        'data': 有新数据写入
                        'drain': 写入缓冲区已空
                        'error': 发生错误
                        'close': 输出关闭
                        'pipe': 输出被管道传输
                        'unpipe': 输出取消管道传输
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
    def exists(self) -> bool:
        """
        检查输出是否存在。

        Returns:
            bool: 如果输出存在，则返回 True，否则返回 False。
        """
        pass

    @abstractmethod
    async def remove(self) -> None:
        """
        删除输出。
        """
        pass

    @abstractmethod
    async def copy(self, dest: 'OutputInterface') -> None:
        """
        将输出复制到另一个输出。

        Args:
            dest (OutputInterface): 目标输出。
        """
        pass

    @abstractmethod
    async def move(self, dest: 'OutputInterface') -> None:
        """
        将输出移动到另一个输出。

        Args:
            dest (OutputInterface): 目标输出。
        """
        pass

    @abstractmethod
    async def rename(self, new_name: str) -> None:
        """
        重命名输出。

        Args:
            new_name (str): 新的输出名称。
        """
        pass

    @abstractmethod
    def get_path(self) -> str:
        """
        获取输出的路径。

        Returns:
            str: 输出的路径。
        """
        pass

    @abstractmethod
    def set_path(self, path: str) -> None:
        """
        设置输出的路径。

        Args:
            path (str): 输出的路径。
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """
        获取输出的名称。

        Returns:
            str: 输出的名称。
        """
        pass

    @abstractmethod
    def set_name(self, name: str) -> None:
        """
        设置输出的名称。

        Args:
            name (str): 输出的名称。
        """
        pass

    @abstractmethod
    def get_extension(self) -> str:
        """
        获取输出的扩展名。

        Returns:
            str: 输出的扩展名。
        """
        pass

    @abstractmethod
    def set_extension(self, extension: str) -> None:
        """
        设置输出的扩展名。

        Args:
            extension (str): 输出的扩展名。
        """
        pass 