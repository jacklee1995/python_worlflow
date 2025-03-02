from typing import Any, List, Dict, Optional, Callable, AsyncIterator
import asyncio
import time
from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from asyncio import StreamWriter

from workflow_engine.interfaces.output_strategy import OutputStrategy
from workflow_engine.interfaces.output_types import OutputErrorType, RetryPolicy, OutputMetrics


class DatabaseOutputStrategy(OutputStrategy):
    """
    数据库输出策略，将数据输出到数据库。
    """

    def __init__(self, db_url: str, table_name: str, if_exists: str = 'append'):
        """
        初始化 DatabaseOutputStrategy。

        Args:
            db_url (str): 数据库连接 URL。
            table_name (str): 输出表名。
            if_exists (str): 表已存在时的处理方式，可选值为 'fail'、'replace'、'append'。
        """
        self._db_url = db_url
        self._table_name = table_name
        self._if_exists = if_exists
        self._writer: Optional[StreamWriter] = None
        self._buffer_size = 64 * 1024  # 64KB
        self._buffer: List[bytes] = []
        self._closing = False
        self._closed = False
        self._buffering_enabled = True
        self._metrics = OutputMetrics()
        self._retry_policy = RetryPolicy()
        self._error_stats: Dict[OutputErrorType, int] = {t: 0 for t in OutputErrorType}
        self._event_handlers = {
            'data': [],
            'drain': [],
            'error': [],
            'close': [],
        }
        self._chained_strategies: List[OutputStrategy] = []
        self._engine = create_engine(db_url)
        self._session = sessionmaker(bind=self._engine)()
        self._metadata = MetaData()
        self._table = None
        self._columns = []

    async def open(self) -> None:
        if not self._table:
            await self._create_table()

    async def get_writer(self) -> StreamWriter:
        if not self._writer:
            await self.open()
        return self._writer

    async def write(self, data: bytes) -> None:
        try:
            if self._buffering_enabled and len(self._buffer) < self._buffer_size:
                self._buffer.append(data)
            else:
                await self._flush_buffer()
                self._buffer = [data]

            self._metrics.bytes_written += len(data)
            self._metrics.write_count += 1
            self._metrics.write_speed = len(data) / (time.time() - self._metrics.last_write_time)
            self._metrics.last_write_time = time.time()

            for handler in self._event_handlers['data']:
                handler(data)
        except Exception as e:
            await self.handle_error(e)

    async def write_batch(self, data: List[bytes], chunk_size: int = 8192) -> None:
        for chunk in data:
            await self.write(chunk)

    async def drain(self) -> None:
        await self._flush_buffer()
        for handler in self._event_handlers['drain']:
            handler()

    async def flush(self) -> None:
        await self._flush_buffer()

    async def write_eof(self) -> None:
        await self._flush_buffer()

    async def close(self) -> None:
        self._closing = True
        await self._flush_buffer()
        self._session.close()
        self._engine.dispose()
        for handler in self._event_handlers['close']:
            handler()

    async def wait_closed(self) -> None:
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
        self._metrics.error_count += 1
        
        if error_type in self._retry_policy.retry_on:
            for i in range(self._retry_policy.max_retries):
                try:
                    delay = min(
                        self._retry_policy.backoff_factor * (2 ** i),
                        self._retry_policy.max_delay
                    )
                    await asyncio.sleep(delay)
                    await self._flush_buffer()
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
        self._error_stats = {t: 0 for t in OutputErrorType}

    async def read_chunks(self, chunk_size: int = 8192) -> AsyncIterator[bytes]:
        for chunk in self._buffer:
            yield chunk

    async def _flush_buffer(self) -> None:
        if not self._buffer:
            return

        try:
            data = b''.join(self._buffer)
            await self._write_to_db(data)
            self._buffer.clear()
        except Exception as e:
            await self.handle_error(e)

    async def _write_to_db(self, data: bytes) -> None:
        try:
            decoded_data = data.decode('utf-8')
            # 这里需要根据实际数据格式进行解析和处理
            # 示例中假设数据是JSON格式
            import json
            record = json.loads(decoded_data)
            self._session.execute(self._table.insert(), [record])
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e

    async def _create_table(self) -> None:
        # 这里需要根据实际需求实现表创建逻辑
        pass

    def _classify_error(self, error: Exception) -> OutputErrorType:
        if isinstance(error, SQLAlchemyError):
            return OutputErrorType.DATABASE_ERROR
        elif isinstance(error, ConnectionError):
            return OutputErrorType.CONNECTION_ERROR
        elif isinstance(error, TimeoutError):
            return OutputErrorType.TIMEOUT_ERROR
        elif isinstance(error, PermissionError):
            return OutputErrorType.PERMISSION_ERROR
        return OutputErrorType.INVALID_DATA 