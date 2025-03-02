from typing import Any, Dict, Optional, Callable, List, Union
import os
import shutil
import json
import time
import asyncio
from asyncio import StreamWriter

from workflow_engine.interfaces.output_interface import OutputInterface
from workflow_engine.interfaces.output_types import OutputErrorType, RetryPolicy, OutputMetrics
from workflow_engine.interfaces.output_strategy import OutputStrategy


class Output(OutputInterface):
    """
    输出类，使用策略模式支持多种输出方式。
    """

    def __init__(self, strategy: OutputStrategy, path: str = None):
        """
        初始化 Output。

        Args:
            strategy (OutputStrategy): 输出策略。
            path (str): 输出路径。
        """
        self._strategy = strategy
        self._path = path
        self._writer: Optional[StreamWriter] = None
        self._event_handlers: Dict[str, list[Callable]] = {
            'data': [],
            'drain': [],
            'error': [],
            'close': [],
            'pipe': [],
            'unpipe': []
        }
        self._closing = False
        self._closed = False
        self._event_handling_enabled = True
        self._encoding = 'utf-8'
        self._timeout = 30.0
        self._metrics = OutputMetrics()
        self._retry_policy = RetryPolicy()
        self._strategies: List[OutputStrategy] = [strategy]
        self._resource_tracking = set()

    async def __aenter__(self) -> 'Output':
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        await self.wait_closed()

    async def open(self) -> None:
        """
        打开输出目标。
        """
        await self._strategy.open()
        self._writer = await self._strategy.get_writer()
        self._resource_tracking.add(self._writer)

    async def get_writer(self) -> StreamWriter:
        """
        获取输出流写入器。

        Returns:
            StreamWriter: 输出流写入器。
        """
        if not self._writer:
            await self.open()
        return self._writer

    async def write(self, data: bytes) -> None:
        """
        将数据写入输出目标。

        Args:
            data (bytes): 要写入的数据。
        """
        try:
            writer = await self.get_writer()
            start_time = time.time()
            
            for strategy in self._strategies:
                await strategy.write(data)
                
            if self._event_handling_enabled:
                for handler in self._event_handlers['data']:
                    handler(data)
                    
            elapsed_time = time.time() - start_time
            self._metrics.bytes_written += len(data)
            self._metrics.write_count += 1
            self._metrics.write_speed = len(data) / max(elapsed_time, 0.001)
            self._metrics.last_write_time = time.time()
            
        except Exception as e:
            self._metrics.error_count += 1
            await self._handle_error(e)

    async def write_batch(self, data: List[bytes], chunk_size: int = 8192) -> None:
        for chunk in data:
            if len(chunk) > chunk_size:
                for i in range(0, len(chunk), chunk_size):
                    await self.write(chunk[i:i + chunk_size])
            else:
                await self.write(chunk)

    async def drain(self) -> None:
        """
        等待输出流完全写入。
        """
        await self._strategy.drain()
        if self._event_handling_enabled:
            for handler in self._event_handlers['drain']:
                handler()

    async def flush(self) -> None:
        for strategy in self._strategies:
            await strategy.flush()

    async def write_eof(self) -> None:
        """
        写入EOF（文件结束）标记。
        """
        await self._strategy.write_eof()

    async def close(self) -> None:
        """
        关闭输出目标，释放资源。
        """
        self._closing = True
        for strategy in self._strategies:
            await strategy.close()
        if self._event_handling_enabled:
            for handler in self._event_handlers['close']:
                handler()

    async def wait_closed(self) -> None:
        """
        等待输出目标完全关闭。
        """
        for strategy in self._strategies:
            await strategy.wait_closed()
        self._closed = True
        self._resource_tracking.clear()

    def is_closing(self) -> bool:
        """
        检查输出目标是否正在关闭。

        Returns:
            bool: 如果输出目标正在关闭，则返回 True，否则返回 False。
        """
        return self._closing

    async def pipe(self, destination: 'OutputInterface', end: bool = True) -> None:
        """
        将输出流管道到另一个输出目标。

        Args:
            destination (OutputInterface): 目标输出。
        """
        if self._event_handling_enabled:
            for handler in self._event_handlers['pipe']:
                handler(destination)
        
        writer = await destination.get_writer()
        for strategy in self._strategies:
            async for chunk in strategy.read_chunks():
                await destination.write(chunk)
                await destination.drain()
        
        if end:
            await destination.write_eof()

    def writable(self) -> bool:
        """
        检查输出目标是否可写。

        Returns:
            bool: 如果输出目标可写，则返回 True，否则返回 False。
        """
        return all(strategy.writable() for strategy in self._strategies)

    def closed(self) -> bool:
        """
        检查输出目标是否已关闭。

        Returns:
            bool: 如果输出目标已关闭，则返回 True，否则返回 False。
        """
        return self._closed

    def get_buffer_size(self) -> int:
        """
        获取输出缓冲区大小。

        Returns:
            int: 输出缓冲区大小。
        """
        return self._strategy.get_buffer_size()

    def set_buffer_size(self, size: int) -> None:
        """
        设置输出缓冲区大小。

        Args:
            size (int): 输出缓冲区大小。
        """
        for strategy in self._strategies:
            strategy.set_buffer_size(size)

    def enable_event_handling(self) -> None:
        self._event_handling_enabled = True

    def disable_event_handling(self) -> None:
        self._event_handling_enabled = False

    def set_retry_policy(self, policy: RetryPolicy) -> None:
        self._retry_policy = policy
        for strategy in self._strategies:
            strategy.set_retry_policy(policy)

    def get_retry_policy(self) -> RetryPolicy:
        return self._retry_policy

    def add_strategy(self, strategy: OutputStrategy) -> None:
        self._strategies.append(strategy)

    def remove_strategy(self, strategy: OutputStrategy) -> None:
        self._strategies.remove(strategy)

    def get_metrics(self) -> OutputMetrics:
        return self._metrics

    def reset_metrics(self) -> None:
        self._metrics = OutputMetrics()

    def is_resource_leak(self) -> bool:
        return len(self._resource_tracking) > 0 and self._closed

    async def write_text(self, text: str, encoding: str = None) -> None:
        encoding = encoding or self._encoding
        await self.write(text.encode(encoding))

    async def write_json(self, data: Any, indent: Optional[int] = None) -> None:
        json_str = json.dumps(data, indent=indent)
        await self.write_text(json_str)

    async def write_lines(self, lines: List[str], encoding: str = None) -> None:
        encoding = encoding or self._encoding
        for line in lines:
            await self.write_text(line + '\n', encoding)

    def set_encoding(self, encoding: str) -> None:
        self._encoding = encoding

    def get_encoding(self) -> str:
        return self._encoding

    def set_timeout(self, timeout: float) -> None:
        self._timeout = timeout

    def get_timeout(self) -> float:
        return self._timeout

    async def _handle_error(self, error: Exception) -> None:
        error_type = self._classify_error(error)
        if error_type in self._retry_policy.retry_on:
            await self._retry_operation()
        if self._event_handling_enabled:
            for handler in self._event_handlers['error']:
                handler(error)
        raise error

    def _classify_error(self, error: Exception) -> OutputErrorType:
        if isinstance(error, ConnectionError):
            return OutputErrorType.CONNECTION_ERROR
        elif isinstance(error, TimeoutError):
            return OutputErrorType.TIMEOUT_ERROR
        elif isinstance(error, PermissionError):
            return OutputErrorType.PERMISSION_ERROR
        elif isinstance(error, OSError):
            return OutputErrorType.FILE_SYSTEM_ERROR
        return OutputErrorType.INVALID_DATA

    async def _retry_operation(self) -> None:
        for i in range(self._retry_policy.max_retries):
            try:
                delay = min(
                    self._retry_policy.backoff_factor * (2 ** i),
                    self._retry_policy.max_delay
                )
                await asyncio.sleep(delay)
                self._metrics.retry_count += 1
                return
            except Exception:
                continue

    def on(self, event: str, callback: Callable) -> None:
        """
        注册事件处理程序。

        Args:
            event (str): 事件名称。
            callback (Callable): 事件处理程序。
        """
        if event not in self._event_handlers:
            raise ValueError(f"Unsupported event: {event}")
        self._event_handlers[event].append(callback)

    def off(self, event: str, callback: Optional[Callable] = None) -> None:
        """
        注销事件处理程序。

        Args:
            event (str): 事件名称。
            callback (Callable): 事件处理程序。
        """
        if event not in self._event_handlers:
            raise ValueError(f"Unsupported event: {event}")
        if callback is None:
            self._event_handlers[event].clear()
        else:
            self._event_handlers[event] = [
                h for h in self._event_handlers[event] if h != callback
            ]

    def exists(self) -> bool:
        """
        检查输出是否存在。

        Returns:
            bool: 如果输出存在，则返回 True，否则返回 False。
        """
        return os.path.exists(self._path) if self._path else False

    async def remove(self) -> None:
        """
        删除输出。
        """
        if self.exists():
            if os.path.isfile(self._path):
                os.remove(self._path)
            elif os.path.isdir(self._path):
                shutil.rmtree(self._path)

    def copy(self, dest: 'OutputInterface') -> None:
        """
        将输出复制到另一个输出。

        Args:
            dest (OutputInterface): 目标输出。
        """
        if not self._path:
            raise ValueError("Source path not set")
        if os.path.isfile(self._path):
            shutil.copy(self._path, dest.get_path())
        elif os.path.isdir(self._path):
            shutil.copytree(self._path, dest.get_path())

    def move(self, dest: 'OutputInterface') -> None:
        """
        将输出移动到另一个输出。

        Args:
            dest (OutputInterface): 目标输出。
        """
        if not self._path:
            raise ValueError("Source path not set")
        shutil.move(self._path, dest.get_path())
        self._path = dest.get_path()

    def rename(self, new_name: str) -> None:
        """
        重命名输出。

        Args:
            new_name (str): 新的输出名称。
        """
        if not self._path:
            raise ValueError("Path not set")
        new_path = os.path.join(os.path.dirname(self._path), new_name)
        os.rename(self._path, new_path)
        self._path = new_path

    def get_path(self) -> str:
        """
        获取输出的路径。

        Returns:
            str: 输出的路径。
        """
        if not self._path:
            raise ValueError("Path not set")
        return self._path

    def set_path(self, path: str) -> None:
        """
        设置输出的路径。

        Args:
            path (str): 输出的路径。
        """
        self._path = path

    def get_name(self) -> str:
        """
        获取输出的名称。

        Returns:
            str: 输出的名称。
        """
        if not self._path:
            raise ValueError("Path not set")
        return os.path.basename(self._path)

    def set_name(self, name: str) -> None:
        """
        设置输出的名称。

        Args:
            name (str): 输出的名称。
        """
        self.rename(name)

    def get_extension(self) -> str:
        """
        获取输出的扩展名。

        Returns:
            str: 输出的扩展名。
        """
        if not self._path:
            raise ValueError("Path not set")
        _, ext = os.path.splitext(self._path)
        return ext

    def set_extension(self, extension: str) -> None:
        """
        设置输出的扩展名。

        Args:
            extension (str): 输出的扩展名。
        """
        if not self._path:
            raise ValueError("Path not set")
        base, _ = os.path.splitext(self._path)
        new_path = f"{base}{extension}"
        os.rename(self._path, new_path)
        self._path = new_path 