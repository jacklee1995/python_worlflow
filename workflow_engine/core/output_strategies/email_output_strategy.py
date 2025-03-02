import smtplib
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import List, Optional, Dict, AsyncIterator, Callable
from asyncio import StreamWriter
import aiosmtplib

from workflow_engine.interfaces.output_strategy import OutputStrategy
from workflow_engine.interfaces.output_types import OutputErrorType, RetryPolicy, OutputMetrics


class EmailOutputStrategy(OutputStrategy):
    """
    邮件输出策略，将数据通过邮件发送。
    """

    def __init__(self, smtp_host: str, smtp_port: int, smtp_username: str, smtp_password: str,
                 from_email: str, to_emails: List[str], subject: str = "Workflow Output",
                 cc_emails: Optional[List[str]] = None, bcc_emails: Optional[List[str]] = None,
                 is_html: bool = False, attachments: Optional[List[str]] = None):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.from_email = from_email
        self.to_emails = to_emails
        self.subject = subject
        self.cc_emails = cc_emails or []
        self.bcc_emails = bcc_emails or []
        self.is_html = is_html
        self.attachments = attachments or []
        
        self._writer: Optional[StreamWriter] = None
        self._buffer_size = 64 * 1024
        self._buffer: List[bytes] = []
        self._buffering_enabled = True
        self._closing = False
        self._closed = False
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
        self._smtp: Optional[aiosmtplib.SMTP] = None

    async def open(self) -> None:
        self._smtp = aiosmtplib.SMTP(hostname=self.smtp_host, port=self.smtp_port)
        await self._smtp.connect()
        await self._smtp.starttls()
        await self._smtp.login(self.smtp_username, self.smtp_password)

    async def get_writer(self) -> StreamWriter:
        if not self._writer:
            loop = asyncio.get_event_loop()
            transport, protocol = await loop.create_connection(
                lambda: asyncio.StreamReaderProtocol(asyncio.StreamReader()),
                self.smtp_host,
                self.smtp_port
            )
            self._writer = StreamWriter(transport, protocol, None, loop)
        return self._writer

    async def write(self, data: bytes) -> None:
        if self._buffering_enabled:
            self._buffer.append(data)
            if sum(len(chunk) for chunk in self._buffer) >= self._buffer_size:
                await self.flush()
        else:
            await self._send_email(data)
        self._metrics.bytes_written += len(data)
        self._metrics.write_count += 1

    async def write_batch(self, data: List[bytes], chunk_size: int = 8192) -> None:
        for chunk in data:
            await self.write(chunk)

    async def drain(self) -> None:
        if self._writer:
            await self._writer.drain()
        for handler in self._event_handlers['drain']:
            handler()

    async def flush(self) -> None:
        if self._buffer:
            combined_data = b''.join(self._buffer)
            await self._send_email(combined_data)
            self._buffer.clear()

    async def write_eof(self) -> None:
        await self.flush()
        if self._writer:
            self._writer.write_eof()

    async def close(self) -> None:
        await self.flush()
        self._closing = True
        if self._smtp:
            await self._smtp.quit()
        if self._writer:
            self._writer.close()
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
        if not self._buffer:
            return 0.0
        return sum(len(chunk) for chunk in self._buffer) / self._buffer_size

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
        for handler in self._event_handlers['error']:
            handler(error)
        if error_type in self._retry_policy.retry_on:
            await self._retry_operation()
        else:
            raise error

    def get_error_stats(self) -> Dict[OutputErrorType, int]:
        return self._error_stats.copy()

    def clear_error_stats(self) -> None:
        self._error_stats = {t: 0 for t in OutputErrorType}

    async def read_chunks(self, chunk_size: int = 8192) -> AsyncIterator[bytes]:
        for chunk in self._buffer:
            yield chunk

    async def _send_email(self, data: bytes) -> None:
        try:
            message = MIMEMultipart()
            message["From"] = self.from_email
            message["To"] = ", ".join(self.to_emails)
            message["Subject"] = self.subject

            if self.cc_emails:
                message["Cc"] = ", ".join(self.cc_emails)

            body = MIMEText(data.decode(), "html" if self.is_html else "plain")
            message.attach(body)

            for attachment in self.attachments:
                with open(attachment, "rb") as file:
                    part = MIMEApplication(file.read(), Name=attachment)
                    part["Content-Disposition"] = f'attachment; filename="{attachment}"'
                    message.attach(part)

            await self._smtp.send_message(message)

            for strategy in self._chained_strategies:
                await strategy.write(data)

        except Exception as e:
            await self.handle_error(e)

    def _classify_error(self, error: Exception) -> OutputErrorType:
        if isinstance(error, aiosmtplib.SMTPConnectError):
            return OutputErrorType.CONNECTION_ERROR
        elif isinstance(error, aiosmtplib.SMTPTimeoutError):
            return OutputErrorType.TIMEOUT_ERROR
        elif isinstance(error, aiosmtplib.SMTPAuthenticationError):
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

    def set_subject(self, subject: str) -> None:
        self.subject = subject

    def get_subject(self) -> str:
        return self.subject

    def set_from_email(self, from_email: str) -> None:
        self.from_email = from_email

    def get_from_email(self) -> str:
        return self.from_email

    def set_to_emails(self, to_emails: List[str]) -> None:
        self.to_emails = to_emails

    def get_to_emails(self) -> List[str]:
        return self.to_emails

    def add_to_email(self, to_email: str) -> None:
        self.to_emails.append(to_email)

    def remove_to_email(self, to_email: str) -> None:
        self.to_emails.remove(to_email)

    def set_cc_emails(self, cc_emails: List[str]) -> None:
        self.cc_emails = cc_emails

    def get_cc_emails(self) -> List[str]:
        return self.cc_emails

    def add_cc_email(self, cc_email: str) -> None:
        self.cc_emails.append(cc_email)

    def remove_cc_email(self, cc_email: str) -> None:
        self.cc_emails.remove(cc_email)

    def set_bcc_emails(self, bcc_emails: List[str]) -> None:
        self.bcc_emails = bcc_emails

    def get_bcc_emails(self) -> List[str]:
        return self.bcc_emails

    def add_bcc_email(self, bcc_email: str) -> None:
        self.bcc_emails.append(bcc_email)

    def remove_bcc_email(self, bcc_email: str) -> None:
        self.bcc_emails.remove(bcc_email)

    def set_is_html(self, is_html: bool) -> None:
        self.is_html = is_html

    def get_is_html(self) -> bool:
        return self.is_html

    def set_attachments(self, attachments: List[str]) -> None:
        self.attachments = attachments

    def get_attachments(self) -> List[str]:
        return self.attachments

    def add_attachment(self, attachment: str) -> None:
        self.attachments.append(attachment)

    def remove_attachment(self, attachment: str) -> None:
        self.attachments.remove(attachment) 