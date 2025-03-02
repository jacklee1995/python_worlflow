import sys
from datetime import datetime
from enum import Enum
from typing import Any, List, Dict, Optional, Callable, AsyncIterator
import asyncio
from asyncio import StreamWriter
import time
from colorama import Fore, Style, init
import json

from workflow_engine.interfaces.output_strategy import OutputStrategy
from workflow_engine.interfaces.output_types import OutputErrorType, RetryPolicy, OutputMetrics


class LogLevel(Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class ConsoleOutputStrategy(OutputStrategy):
    """
    控制台输出策略，将数据输出到控制台。
    """

    def __init__(self, log_level: LogLevel = LogLevel.INFO, timestamp_format: str = "%Y-%m-%d %H:%M:%S"):
        self._writer: Optional[StreamWriter] = None
        self._buffer_size = 64 * 1024  # 64KB
        self._buffer: List[bytes] = []
        self._buffering_enabled = True
        self._closing = False
        self._closed = False
        self._metrics = OutputMetrics()
        self._retry_policy = RetryPolicy()
        self._error_stats: Dict[OutputErrorType, int] = {err: 0 for err in OutputErrorType}
        self._chained_strategies: List[OutputStrategy] = []
        self._event_handlers = {
            'data': [],
            'drain': [],
            'error': [],
            'close': [],
        }
        self.log_level = log_level
        self.timestamp_format = timestamp_format
        init(autoreset=True)

    async def open(self) -> None:
        # 不需要特殊的初始化
        pass

    async def get_writer(self) -> StreamWriter:
        # 不需要 writer
        return None

    async def write(self, data: bytes | dict) -> None:
        try:
            if self._buffering_enabled and len(self._buffer) < self._buffer_size:
                self._buffer.append(data)
            else:
                await self._flush_buffer()
                timestamp = datetime.now().strftime(self.timestamp_format)
                color = self._get_color(self.log_level)
                
                # 处理不同类型的数据
                if isinstance(data, dict):
                    message = json.dumps(data, indent=2)
                elif isinstance(data, bytes):
                    message = data.decode()
                else:
                    message = str(data)
                    
                log_message = f"{color}[{timestamp}] {message}{Style.RESET_ALL}\n"
                print(log_message, end='', flush=True)
                
            self._metrics.bytes_written += len(str(data))
            self._metrics.write_count += 1
            self._metrics.write_speed = len(str(data)) / 0.001  # 假设写入时间为1ms
            self._metrics.last_write_time = time.time()
            
            for handler in self._event_handlers['data']:
                handler(data)
        except Exception as e:
            self._error_stats[self._classify_error(e)] += 1
            self._metrics.error_count += 1
            await self.handle_error(e)

    async def write_batch(self, data: List[bytes], chunk_size: int = 8192) -> None:
        for chunk in data:
            await self.write(chunk)

    async def drain(self) -> None:
        await self._flush_buffer()
        sys.stdout.flush()

    async def flush(self) -> None:
        await self._flush_buffer()

    async def _flush_buffer(self) -> None:
        if self._buffer:
            for data in self._buffer:
                timestamp = datetime.now().strftime(self.timestamp_format)
                color = self._get_color(self.log_level)
                
                # 处理不同类型的数据
                if isinstance(data, dict):
                    message = json.dumps(data, indent=2)
                elif isinstance(data, bytes):
                    message = data.decode()
                else:
                    message = str(data)
                    
                log_message = f"{color}[{timestamp}] {message}{Style.RESET_ALL}\n"
                print(log_message, end='', flush=True)
            self._buffer.clear()

    async def write_eof(self) -> None:
        await self._flush_buffer()

    async def close(self) -> None:
        await self._flush_buffer()
        self._closing = True
        for handler in self._event_handlers['close']:
            handler()

    async def wait_closed(self) -> None:
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

    def get_metrics(self) -> OutputMetrics:
        return self._metrics

    def reset_metrics(self) -> None:
        self._metrics = OutputMetrics()

    def set_retry_policy(self, policy: RetryPolicy) -> None:
        self._retry_policy = policy

    def get_retry_policy(self) -> RetryPolicy:
        return self._retry_policy

    def enable_buffering(self) -> None:
        self._buffering_enabled = True

    def disable_buffering(self) -> None:
        self._buffering_enabled = False

    def get_buffer_usage(self) -> float:
        return len(self._buffer) / self._buffer_size if self._buffer_size > 0 else 0.0

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
        if strategy in self._chained_strategies:
            self._chained_strategies.remove(strategy)

    def get_chained_strategies(self) -> List['OutputStrategy']:
        return self._chained_strategies.copy()

    async def handle_error(self, error: Exception) -> None:
        error_type = self._classify_error(error)
        if error_type in self._retry_policy.retry_on:
            await self._retry_operation()
        for handler in self._event_handlers['error']:
            handler(error)

    def get_error_stats(self) -> Dict[OutputErrorType, int]:
        return self._error_stats.copy()

    def clear_error_stats(self) -> None:
        self._error_stats = {err: 0 for err in OutputErrorType}

    async def read_chunks(self, chunk_size: int = 8192) -> AsyncIterator[bytes]:
        for chunk in self._buffer:
            yield chunk

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

    def _get_color(self, level: LogLevel) -> str:
        if level == LogLevel.DEBUG:
            return Fore.CYAN
        elif level == LogLevel.INFO:
            return Fore.GREEN
        elif level == LogLevel.WARNING:
            return Fore.YELLOW
        elif level == LogLevel.ERROR:
            return Fore.RED
        elif level == LogLevel.CRITICAL:
            return Fore.MAGENTA
        else:
            return ""

    def set_log_level(self, log_level: LogLevel) -> None:
        self.log_level = log_level

    def get_log_level(self) -> LogLevel:
        return self.log_level

    def set_timestamp_format(self, timestamp_format: str) -> None:
        self.timestamp_format = timestamp_format

    def get_timestamp_format(self) -> str:
        return self.timestamp_format

    def debug(self, message: str) -> None:
        asyncio.create_task(self.write(message.encode()))

    def info(self, message: str) -> None:
        asyncio.create_task(self.write(message.encode()))

    def warning(self, message: str) -> None:
        asyncio.create_task(self.write(message.encode()))

    def error(self, message: str) -> None:
        asyncio.create_task(self.write(message.encode()))

    def critical(self, message: str) -> None:
        asyncio.create_task(self.write(message.encode()))

    def exception(self, message: str) -> None:
        asyncio.create_task(self.write(f"{message}\n{sys.exc_info()[1]}".encode())) 