from typing import List, Optional, AsyncIterator, Callable, Dict
import asyncio
import os
from functools import wraps

from workflow_engine.interfaces.task_interface import TaskInterface
from workflow_engine.interfaces.step_interface import StepInterface
from workflow_engine.interfaces.config_interface import ConfigInterface
from workflow_engine.interfaces.source_interface import SourceInterface
from workflow_engine.interfaces.output_interface import OutputInterface


class Task(TaskInterface):
    """任务实现类，支持异步流式处理"""

    def __init__(self, name: str = 'Task', description: str = 'A workflow task'):
        self._name = name
        self._description = description
        self._steps: List[StepInterface] = []
        self._config: Optional[ConfigInterface] = None
        self._source: Optional[SourceInterface] = None
        self._output: Optional[OutputInterface] = None
        self._env_vars: Dict[str, str] = {}
        self._event_handlers = {
            'start': [],
            'stop': [],
            'pause': [],
            'resume': [],
            'step_start': [],
            'step_complete': [],
            'step_error': []
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

    async def add_step(self, step: StepInterface) -> None:
        self._steps.append(step)
        if self._source:
            step.set_sources([self._source])

    async def remove_step(self, step: StepInterface) -> None:
        self._steps.remove(step)

    def get_steps(self) -> List[StepInterface]:
        return self._steps

    async def execute(self) -> AsyncIterator[bytes]:
        if not self._steps:
            raise ValueError("No steps provided")

        try:
            for handler in self._event_handlers['start']:
                handler()

            for step in self._steps:
                for handler in self._event_handlers['step_start']:
                    handler(step)

                async for chunk in step.process(self._source):
                    if self._stopped:
                        break
                    while self._paused:
                        await asyncio.sleep(0.1)
                    if self._output:
                        await self._output.write(chunk)
                        await self._output.drain()
                    yield chunk

                for handler in self._event_handlers['step_complete']:
                    handler(step)

        except Exception as e:
            for handler in self._event_handlers['step_error']:
                handler(step, e)
            raise
        finally:
            for handler in self._event_handlers['stop']:
                handler()

    async def pipe(self, destination: TaskInterface) -> TaskInterface:
        async def process_and_pipe():
            async for chunk in self.execute():
                await destination.get_output().write(chunk)
                await destination.get_output().drain()
            destination.get_output().write_eof()

        asyncio.create_task(process_and_pipe())
        return destination

    async def series(self, *steps: StepInterface) -> AsyncIterator[bytes]:
        if not steps:
            raise ValueError("At least one step is required for series execution")

        for i in range(len(steps) - 1):
            steps[i].pipe(steps[i + 1])

        self._steps.extend(steps)
        return self.execute()

    async def parallel(self, *steps: StepInterface) -> List[AsyncIterator[bytes]]:
        return [step.process(self._source) for step in steps]

    def set_config(self, config: ConfigInterface) -> None:
        self._config = config

    def get_config(self) -> Optional[ConfigInterface]:
        return self._config

    def set_source(self, source: SourceInterface) -> None:
        self._source = source
        for step in self._steps:
            step.set_sources([source])

    def get_source(self) -> Optional[SourceInterface]:
        return self._source

    def set_output(self, output: OutputInterface) -> None:
        self._output = output

    def get_output(self) -> Optional[OutputInterface]:
        return self._output

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

    def _load_env_vars(self) -> None:
        self._env_vars = dict(os.environ)

    def get_env_var(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return self._env_vars.get(key, default)


def task(func: Callable) -> Callable[[], TaskInterface]:
    """
    任务装饰器，将普通函数转换为 Task 对象。

    该装饰器允许用户使用简单的函数语法定义任务，同时自动将函数转换为 Task 对象。
    装饰器会从函数的元数据中提取名称和描述，并创建一个新的 Task 实例。

    示例：
    ```python
    @task
    async def build():
        \"\"\"构建任务\"\"\"
        # 任务逻辑
        pass
    ```

    参数：
    - func (Callable): 要转换为任务的函数。

    返回值：
    - Callable[[], TaskInterface]: 返回一个创建 Task 实例的工厂函数。
    """
    @wraps(func)
    def task_factory() -> TaskInterface:
        task_instance = Task(func.__name__, func.__doc__ or 'A workflow task')
        task_instance._execute = func  # 保存原始函数
        # 重写 execute 方法
        async def execute_wrapper() -> AsyncIterator[bytes]:
            try:
                await func(task_instance._source, task_instance._output)
                yield b''  # 保持 AsyncIterator 接口
            except Exception as e:
                for handler in task_instance._event_handlers['step_error']:
                    handler(None, e)
                raise
        task_instance.execute = execute_wrapper
        return task_instance
    return task_factory
