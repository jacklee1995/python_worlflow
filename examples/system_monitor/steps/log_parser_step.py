from typing import Dict, Any, List, Optional, AsyncIterator, Callable
from workflow_engine.core.step import Step
from workflow_engine.interfaces.source_interface import SourceInterface
import json
import re
import asyncio

class LogParserStep(Step):
    """
    日志解析步骤。

    解析日志文件，提取错误和警告信息。
    """

    def __init__(self, name: str = 'LogParserStep', description: str = 'Parse logs for errors and warnings'):
        super().__init__(name, description)
        self._event_handlers: Dict[str, List[Callable]] = {
            'data': [],
            'error': [],
            'end': [],
            'pipe': []
        }

    async def execute(self) -> None:
        if not self.get_output():
            raise ValueError("Output not set")

        patterns = self.get_config().get('patterns', {})
        error_pattern = re.compile(patterns.get('error', ''))
        warning_pattern = re.compile(patterns.get('warning', ''))

        for source in self.get_sources():
            await source.open()
            try:
                async for line in source:
                    line_str = line.decode()
                    errors = error_pattern.findall(line_str)
                    warnings = warning_pattern.findall(line_str)

                    if errors or warnings:
                        log_entry = {
                            'line': line_str.strip(),
                            'errors': errors,
                            'warnings': warnings
                        }
                        await self.get_output().write(json.dumps(log_entry, indent=2).encode())
            finally:
                await source.close()

    async def process(self, source: SourceInterface) -> AsyncIterator[bytes]:
        """处理输入流并生成输出流"""
        await source.open()
        try:
            async for chunk in source:
                transformed = await self.transform(chunk)
                if self.get_output():
                    await self.get_output().write(transformed)
                yield transformed
        finally:
            await source.close()

    async def pipe(self, destination: 'Step') -> 'Step':
        """将当前步骤的输出连接到下一个步骤"""
        for handler in self._event_handlers['pipe']:
            handler(destination)
        
        async def process_and_pipe():
            if self.get_output() and self.get_sources():
                await self.get_sources()[0].open()
                try:
                    async for chunk in self.process(self.get_sources()[0]):
                        await destination.get_output().write(chunk)
                        await destination.get_output().drain()
                    await destination.get_output().write_eof()
                finally:
                    await self.get_sources()[0].close()

        asyncio.create_task(process_and_pipe())
        return destination

    async def transform(self, chunk: bytes) -> bytes:
        """转换数据块"""
        return chunk

    def on(self, event: str, callback: Callable) -> None:
        """注册事件处理器"""
        if event not in self._event_handlers:
            raise ValueError(f"Unsupported event: {event}")
        self._event_handlers[event].append(callback)

    def off(self, event: str, callback: Optional[Callable] = None) -> None:
        """移除事件处理器"""
        if event not in self._event_handlers:
            raise ValueError(f"Unsupported event: {event}")
        if callback is None:
            self._event_handlers[event].clear()
        else:
            self._event_handlers[event] = [
                h for h in self._event_handlers[event] if h != callback
            ] 