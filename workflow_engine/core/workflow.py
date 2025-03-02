from typing import List, Dict, Optional, AsyncIterator, Callable
import asyncio

from workflow_engine.interfaces.workflow_interface import WorkflowInterface
from workflow_engine.interfaces.task_interface import TaskInterface
from workflow_engine.interfaces.config_interface import ConfigInterface
from workflow_engine.interfaces.output_interface import OutputInterface
from workflow_engine.interfaces.source_interface import SourceInterface


class Workflow(WorkflowInterface):
    """工作流实现类，支持异步流式处理"""

    def __init__(self, name: str = 'Workflow', description: str = 'A workflow'):
        self._name = name
        self._description = description
        self._tasks: List[TaskInterface] = []
        self._config: Optional[ConfigInterface] = None
        self._source: Optional[SourceInterface] = None
        self._output: Optional[OutputInterface] = None
        self._event_handlers: Dict[str, List[Callable]] = {
            'start': [],
            'stop': [],
            'pause': [],
            'resume': [],
            'task_start': [],
            'task_complete': [],
            'task_error': []
        }
        self._paused = False
        self._stopped = False

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def get_description(self) -> str:
        return self._description

    def set_description(self, description: str) -> None:
        self._description = description

    async def add_task(self, task: TaskInterface) -> None:
        self._tasks.append(task)
        if self._source:
            task.set_source(self._source)

    async def remove_task(self, task: TaskInterface) -> None:
        self._tasks.remove(task)

    def get_tasks(self) -> List[TaskInterface]:
        return self._tasks

    def set_config(self, config: ConfigInterface) -> None:
        self._config = config

    def get_config(self) -> Optional[ConfigInterface]:
        return self._config

    def set_source(self, source: SourceInterface) -> None:
        self._source = source
        for task in self._tasks:
            task.set_source(source)

    def get_source(self) -> Optional[SourceInterface]:
        return self._source

    def set_output(self, output: OutputInterface) -> None:
        self._output = output

    def get_output(self) -> Optional[OutputInterface]:
        return self._output

    async def execute(self) -> AsyncIterator[bytes]:
        if not self._tasks:
            raise ValueError("No tasks provided")

        try:
            for handler in self._event_handlers['start']:
                handler()

            for task in self._tasks:
                for handler in self._event_handlers['task_start']:
                    handler(task)

                async for chunk in task.execute():
                    if self._stopped:
                        break
                    while self._paused:
                        await asyncio.sleep(0.1)
                    if self._output:
                        self._output.write(chunk)
                        await self._output.drain()
                    yield chunk

                for handler in self._event_handlers['task_complete']:
                    handler(task)

        except Exception as e:
            for handler in self._event_handlers['task_error']:
                handler(e)
            raise
        finally:
            for handler in self._event_handlers['stop']:
                handler()

    async def pipe(self, destination: WorkflowInterface) -> WorkflowInterface:
        async def process_and_pipe():
            async for chunk in self.execute():
                await destination.get_output().write(chunk)
                await destination.get_output().drain()
            destination.get_output().write_eof()

        asyncio.create_task(process_and_pipe())
        return destination

    async def series(self, *tasks: TaskInterface) -> AsyncIterator[bytes]:
        if not tasks:
            raise ValueError("At least one task is required for series execution")

        for i in range(len(tasks) - 1):
            await tasks[i].pipe(tasks[i + 1])

        self._tasks.extend(tasks)
        return self.execute()

    async def parallel(self, *tasks: TaskInterface) -> List[AsyncIterator[bytes]]:
        return [task.execute() for task in tasks]

    def pause(self) -> None:
        self._paused = True
        for handler in self._event_handlers['pause']:
            handler()

    def resume(self) -> None:
        self._paused = False
        for handler in self._event_handlers['resume']:
            handler()

    def stop(self) -> None:
        self._stopped = True

    def get_status(self) -> str:
        if self._stopped:
            return 'stopped'
        return 'paused' if self._paused else 'running'

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
