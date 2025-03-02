from typing import List, Optional, AsyncIterator
import asyncio
from functools import wraps

from workflow_engine.interfaces.step_interface import StepInterface
from workflow_engine.interfaces.source_interface import SourceInterface
from workflow_engine.interfaces.config_interface import ConfigInterface
from workflow_engine.interfaces.output_interface import OutputInterface


class Step(StepInterface):
    """
    步骤实现类，支持异步流式处理。
    """

    def __init__(self, name: str = 'Step', description: str = 'A workflow step in task'):
        self._name = name
        self._description = description
        self._config: Optional[ConfigInterface] = None
        self._sources: List[SourceInterface] = []
        self._output: Optional[OutputInterface] = None
        self._event_handlers = {
            'data': [],
            'error': [],
            'end': [],
            'close': [],
            'pipe': [],
            'unpipe': []
        }
        self._paused = False
        self._stopped = False
        self._current_source: Optional[SourceInterface] = None

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def get_description(self) -> str:
        return self._description

    def set_description(self, description: str) -> None:
        self._description = description

    def set_config(self, config: ConfigInterface) -> None:
        self._config = config

    def get_config(self) -> ConfigInterface:
        if self._config is None:
            raise ValueError("Config not set")
        return self._config

    def set_sources(self, sources: List[SourceInterface]) -> None:
        self._sources = sources

    def get_sources(self) -> List[SourceInterface]:
        return self._sources

    def set_output(self, output: OutputInterface) -> None:
        self._output = output

    def get_output(self) -> OutputInterface:
        if self._output is None:
            raise ValueError("Output not set")
        return self._output

    async def execute(self) -> None:
        if not self._sources:
            raise ValueError("No sources provided")

        try:
            async for source in self._sources:
                self._current_source = source
                await source.open()
                async for chunk in source:
                    if self._stopped:
                        break
                    while self._paused:
                        await asyncio.sleep(0.1)
                    transformed = await self.transform(chunk)
                    if self._output:
                        self._output.write(transformed)
                        await self._output.drain()
                    for handler in self._event_handlers['data']:
                        handler(transformed)
                if self._output:
                    self._output.write_eof()
                for handler in self._event_handlers['end']:
                    handler()
        except Exception as e:
            for handler in self._event_handlers['error']:
                handler(e)
            raise
        finally:
            if self._current_source:
                self._current_source.close()
                await self._current_source.wait_closed()
            for handler in self._event_handlers['close']:
                handler()

    async def process(self, source: SourceInterface) -> AsyncIterator[bytes]:
        async for chunk in source:
            yield await self.transform(chunk)

    async def pipe(self, destination: StepInterface) -> StepInterface:
        for handler in self._event_handlers['pipe']:
            handler(destination)

        async def process_and_pipe():
            async for chunk in self.process(self._current_source):
                await destination.get_output().write(chunk)
                await destination.get_output().drain()
            destination.get_output().write_eof()

        asyncio.create_task(process_and_pipe())
        return destination

    async def transform(self, chunk: bytes) -> bytes:
        return chunk

    def on(self, event: str, callback: callable) -> None:
        if event not in self._event_handlers:
            raise ValueError(f"Unsupported event: {event}")
        self._event_handlers[event].append(callback)

    def off(self, event: str, callback: Optional[callable] = None) -> None:
        if event not in self._event_handlers:
            raise ValueError(f"Unsupported event: {event}")
        if callback is None:
            self._event_handlers[event].clear()
        else:
            self._event_handlers[event] = [
                h for h in self._event_handlers[event] if h != callback
            ]

    def pause(self) -> None:
        self._paused = True

    def resume(self) -> None:
        self._paused = False

    def stop(self) -> None:
        self._stopped = True
