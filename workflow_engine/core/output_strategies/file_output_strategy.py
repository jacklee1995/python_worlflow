import asyncio
import os
import json
from datetime import datetime
from typing import Any, List, Dict, Optional, Callable, AsyncIterator
from asyncio import StreamWriter

from workflow_engine.interfaces.output_strategy import OutputStrategy
from workflow_engine.interfaces.output_types import OutputErrorType, RetryPolicy, OutputMetrics


class FileOutputStrategy(OutputStrategy):
    """
    文件输出策略，将数据输出到文件。
    """

    def __init__(self, file_path: str, append: bool = False, 
                 timestamp_format: str = "%Y-%m-%d %H:%M:%S",
                 buffer_size: int = 64 * 1024):
        self.file_path = file_path
        self.append = append
        self.timestamp_format = timestamp_format
        self._buffer_size = buffer_size
        self._file = None
        self._closing = False
        self._closed = False
        self._metrics = OutputMetrics()
        self._retry_policy = RetryPolicy()
        self._error_stats: Dict[OutputErrorType, int] = {
            error_type: 0 for error_type in OutputErrorType
        }
        self._event_handlers = {
            'data': [],
            'drain': [],
            'error': [],
            'close': []
        }
        self._chained_strategies: List[OutputStrategy] = []
        self._ensure_dir()

    def _ensure_dir(self):
        """确保输出目录存在"""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    async def open(self) -> None:
        """打开输出文件"""
        mode = 'a' if self.append else 'w'
        self._file = open(self.file_path, mode, encoding='utf-8')

    async def get_writer(self) -> None:
        """这个方法在这里不会被使用，但需要实现接口"""
        return None

    async def write(self, data: bytes) -> None:
        """写入数据到文件"""
        if not self._file:
            await self.open()
        
        try:
            # 解码并解析JSON数据
            json_data = json.loads(data.decode())
            
            # 添加时间戳
            output_data = {
                'timestamp': datetime.now().strftime(self.timestamp_format),
                'data': json_data
            }
            
            # 写入文件
            self._file.write(json.dumps(output_data, indent=2) + '\n')
            
            self._metrics.bytes_written += len(data)
            self._metrics.write_count += 1
            
            for handler in self._event_handlers['data']:
                handler(data)
        except Exception as e:
            self._metrics.error_count += 1
            await self.handle_error(e)

    async def write_batch(self, data: List[bytes], chunk_size: int = 8192) -> None:
        """批量写入数据"""
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            await self.write(b''.join(chunk))

    async def drain(self) -> None:
        """等待写入缓冲区清空"""
        if self._file:
            self._file.flush()
            for handler in self._event_handlers['drain']:
                handler()

    async def flush(self) -> None:
        """刷新缓冲区数据到文件"""
        if self._file:
            self._file.flush()

    async def write_eof(self) -> None:
        """写入EOF标记(在这里不需要)"""
        pass

    async def close(self) -> None:
        """关闭输出文件"""
        if self._file and not self._file.closed:
            self._closing = True
            await self.flush()
            self._file.close()
            self._closed = True
            for handler in self._event_handlers['close']:
                handler()

    async def wait_closed(self) -> None:
        """等待文件完全关闭"""
        while not self._closed:
            await asyncio.sleep(0.1)

    def is_closing(self) -> bool:
        return self._closing

    def writable(self) -> bool:
        return self._file is not None and not self._closing

    def closed(self) -> bool:
        return self._closed

    def get_buffer_size(self) -> int:
        return self._buffer_size

    def set_buffer_size(self, size: int) -> None:
        self._buffer_size = size

    def enable_buffering(self) -> None:
        """启用缓冲区(在这里不需要)"""
        pass

    def disable_buffering(self) -> None:
        """禁用缓冲区(在这里不需要)"""
        pass

    def get_metrics(self) -> OutputMetrics:
        return self._metrics

    def clear_metrics(self) -> None:
        self._metrics = OutputMetrics()

    def get_retry_policy(self) -> RetryPolicy:
        return self._retry_policy

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

    async def chain(self, next_strategy: 'OutputStrategy') -> None:
        self._chained_strategies.append(next_strategy)

    async def unchain(self, strategy: 'OutputStrategy') -> None:
        self._chained_strategies.remove(strategy)

    def get_chained_strategies(self) -> List['OutputStrategy']:
        return self._chained_strategies.copy()

    async def handle_error(self, error: Exception) -> None:
        error_type = self._classify_error(error)
        self._error_stats[error_type] += 1
        if error_type in self._retry_policy.retry_on:
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
        for handler in self._event_handlers['error']:
            handler(error)
        raise error

    def get_error_stats(self) -> Dict[OutputErrorType, int]:
        return self._error_stats.copy()

    def clear_error_stats(self) -> None:
        for key in self._error_stats:
            self._error_stats[key] = 0

    async def read_chunks(self, chunk_size: int = 8192) -> AsyncIterator[bytes]:
        if os.path.exists(self.file_path):
            with open(self.file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk

    def _classify_error(self, error: Exception) -> OutputErrorType:
        """对错误进行分类"""
        if isinstance(error, PermissionError):
            return OutputErrorType.PERMISSION_ERROR
        elif isinstance(error, OSError):
            return OutputErrorType.FILE_SYSTEM_ERROR
        elif isinstance(error, IOError):
            return OutputErrorType.FILE_SYSTEM_ERROR
        return OutputErrorType.INVALID_DATA

    def get_buffer_usage(self) -> int:
        """获取缓冲区使用情况(在这里不需要)"""
        return 0

    def reset_metrics(self) -> None:
        """重置指标(与clear_metrics功能相同)"""
        self.clear_metrics()

    def set_retry_policy(self, policy: RetryPolicy) -> None:
        """设置重试策略"""
        self._retry_policy = policy 