import logging
from typing import Any, Dict, Optional, List, AsyncIterator, Callable
import asyncio
from asyncio import StreamWriter
import time

from workflow_engine.interfaces.output_strategy import OutputStrategy
from workflow_engine.interfaces.output_types import OutputErrorType, RetryPolicy, OutputMetrics


class LogOutputStrategy(OutputStrategy):
    """
    日志输出策略，将数据输出到日志系统。
    """

    def __init__(self, logger_name: str = "workflow", level: int = logging.INFO,
                 format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                 datefmt: str = "%Y-%m-%d %H:%M:%S", handlers: Optional[list] = None,
                 filters: Optional[list] = None, extra: Optional[Dict[str, Any]] = None):
        self.logger_name = logger_name
        self.level = level
        self.format = format
        self.datefmt = datefmt
        self.handlers = handlers or []
        self.filters = filters or []
        self.extra = extra or {}
        
        self._writer: Optional[StreamWriter] = None
        self._buffer_size = 64 * 1024
        self._buffer: List[bytes] = []
        self._closing = False
        self._closed = False
        self._buffering_enabled = True
        self._metrics = OutputMetrics()
        self._retry_policy = RetryPolicy()
        self._error_stats: Dict[OutputErrorType, int] = {t: 0 for t in OutputErrorType}
        self._chained_strategies: List[OutputStrategy] = []
        self._event_handlers = {
            'data': [],
            'drain': [],
            'error': [],
            'close': [],
        }

        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(self.level)

        formatter = logging.Formatter(self.format, self.datefmt)
        for handler in self.handlers:
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        for filter in self.filters:
            self.logger.addFilter(filter)

    async def open(self) -> None:
        loop = asyncio.get_event_loop()
        transport, protocol = await loop.connect_write_pipe(
            asyncio.streams.FlowControlMixin,
            asyncio.streams.StreamWriter(self.logger.handlers[0].stream)
        )
        self._writer = StreamWriter(transport, protocol, None, loop)

    async def get_writer(self) -> StreamWriter:
        if not self._writer:
            await self.open()
        return self._writer

    async def write(self, data: bytes) -> None:
        try:
            start_time = time.time()
            if self._buffering_enabled and len(self._buffer) < self._buffer_size:
                self._buffer.append(data)
            else:
                await self._flush_buffer()
                self.logger.log(self.level, data.decode(), extra=self.extra)
            
            self._metrics.bytes_written += len(data)
            self._metrics.write_count += 1
            self._metrics.write_speed = len(data) / (time.time() - start_time)
            self._metrics.last_write_time = time.time()
            
            for handler in self._event_handlers['data']:
                handler(data)
        except Exception as e:
            self._metrics.error_count += 1
            await self.handle_error(e)

    async def write_batch(self, data: List[bytes], chunk_size: int = 8192) -> None:
        for chunk in data:
            await self.write(chunk)

    async def drain(self) -> None:
        if self._writer:
            await self._writer.drain()
            for handler in self._event_handlers['drain']:
                handler()

    async def flush(self) -> None:
        await self._flush_buffer()

    async def write_eof(self) -> None:
        await self._flush_buffer()
        if self._writer:
            self._writer.write_eof()

    async def close(self) -> None:
        self._closing = True
        await self._flush_buffer()
        if self._writer:
            self._writer.close()
        for handler in self.logger.handlers:
            handler.close()
        for handler in self._event_handlers['close']:
            handler()

    async def wait_closed(self) -> None:
        if self._writer:
            await self._writer.wait_closed()
        self._closed = True

    def is_closing(self) -> bool:
        return self._closing

    def writable(self) -> bool:
        return not self._closing and not self._closed

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
        self._chained_strategies.remove(strategy)

    def get_chained_strategies(self) -> List['OutputStrategy']:
        return self._chained_strategies.copy()

    async def handle_error(self, error: Exception) -> None:
        error_type = self._classify_error(error)
        self._error_stats[error_type] += 1
        if error_type in self._retry_policy.retry_on:
            await self._retry_operation()
        for handler in self._event_handlers['error']:
            handler(error)
        raise error

    def get_error_stats(self) -> Dict[OutputErrorType, int]:
        return self._error_stats.copy()

    def clear_error_stats(self) -> None:
        for key in self._error_stats:
            self._error_stats[key] = 0

    async def read_chunks(self, chunk_size: int = 8192) -> AsyncIterator[bytes]:
        for chunk in self._buffer:
            yield chunk
        self._buffer.clear()

    async def _flush_buffer(self) -> None:
        if self._buffer:
            for data in self._buffer:
                self.logger.log(self.level, data.decode(), extra=self.extra)
            self._buffer.clear()

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

    def set_level(self, level: int) -> None:
        self.level = level
        self.logger.setLevel(self.level)

    def get_level(self) -> int:
        return self.level

    def set_format(self, format: str) -> None:
        self.format = format
        formatter = logging.Formatter(self.format, self.datefmt)
        for handler in self.logger.handlers:
            handler.setFormatter(formatter)

    def get_format(self) -> str:
        return self.format

    def set_datefmt(self, datefmt: str) -> None:
        self.datefmt = datefmt
        formatter = logging.Formatter(self.format, self.datefmt)
        for handler in self.logger.handlers:
            handler.setFormatter(formatter)

    def get_datefmt(self) -> str:
        return self.datefmt

    def add_handler(self, handler: logging.Handler) -> None:
        handler.setFormatter(logging.Formatter(self.format, self.datefmt))
        self.logger.addHandler(handler)
        self.handlers.append(handler)

    def remove_handler(self, handler: logging.Handler) -> None:
        self.logger.removeHandler(handler)
        self.handlers.remove(handler)

    def get_handlers(self) -> list:
        return self.handlers

    def add_filter(self, filter: logging.Filter) -> None:
        self.logger.addFilter(filter)
        self.filters.append(filter)

    def remove_filter(self, filter: logging.Filter) -> None:
        self.logger.removeFilter(filter)
        self.filters.remove(filter)

    def get_filters(self) -> list:
        return self.filters

    def set_extra(self, extra: Dict[str, Any]) -> None:
        self.extra = extra

    def get_extra(self) -> Dict[str, Any]:
        return self.extra

    def update_extra(self, extra: Dict[str, Any]) -> None:
        self.extra.update(extra)

    def clear_extra(self) -> None:
        self.extra.clear()

    def log(self, level: int, msg: str, *args, **kwargs) -> None:
        self.logger.log(level, msg, *args, **kwargs)

    def debug(self, msg: str, *args, **kwargs) -> None:
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs) -> None:
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs) -> None:
        self.logger.critical(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs) -> None:
        self.logger.exception(msg, *args, **kwargs) 