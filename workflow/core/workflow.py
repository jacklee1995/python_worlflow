from typing import List, Dict, Optional, Callable
from workflow.interfaces.workflow_interface import WorkflowInterface
from workflow.interfaces.task_interface import TaskInterface
from workflow.interfaces.config_interface import ConfigInterface

class Workflow(WorkflowInterface):
    """
    工作流实现类，用于管理多个任务及其执行顺序。
    """

    def __init__(self, name: str = 'Workflow', description: str = 'A workflow'):
        self.name = name
        self.description = description
        self.tasks: List[TaskInterface] = []
        self.config: Optional[ConfigInterface] = None
        self.status: str = 'stopped'
        self.callbacks: Dict[str, List[Callable]] = {
            'start': [],
            'stop': [],
            'pause': [],
            'resume': [],
            'task_start': [],
            'task_complete': [],
            'task_error': []
        }

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    def get_description(self) -> str:
        return self.description

    def set_description(self, description: str) -> None:
        self.description = description

    def add_task(self, task: TaskInterface) -> None:
        self.tasks.append(task)

    def remove_task(self, task: TaskInterface) -> None:
        self.tasks.remove(task)

    def get_tasks(self) -> List[TaskInterface]:
        return self.tasks

    def set_config(self, config: ConfigInterface) -> None:
        self.config = config

    def get_config(self) -> Optional[ConfigInterface]:
        return self.config

    def execute(self) -> None:
        self.status = 'running'
        self._trigger_callbacks('start')

        for task in self.tasks:
            try:
                self._trigger_callbacks('task_start', task)
                task.execute()
                self._trigger_callbacks('task_complete', task)
            except Exception as e:
                self._trigger_callbacks('task_error', task, e)
                raise

        self.status = 'stopped'
        self._trigger_callbacks('stop')

    def stop(self) -> None:
        self.status = 'stopped'
        self._trigger_callbacks('stop')

    def pause(self) -> None:
        self.status = 'paused'
        self._trigger_callbacks('pause')

    def resume(self) -> None:
        self.status = 'running'
        self._trigger_callbacks('resume')

    def get_status(self) -> str:
        return self.status

    def on_start(self, callback: Callable) -> None:
        self.callbacks['start'].append(callback)

    def on_stop(self, callback: Callable) -> None:
        self.callbacks['stop'].append(callback)

    def on_pause(self, callback: Callable) -> None:
        self.callbacks['pause'].append(callback)

    def on_resume(self, callback: Callable) -> None:
        self.callbacks['resume'].append(callback)

    def on_task_start(self, callback: Callable) -> None:
        self.callbacks['task_start'].append(callback)

    def on_task_complete(self, callback: Callable) -> None:
        self.callbacks['task_complete'].append(callback)

    def on_task_error(self, callback: Callable) -> None:
        self.callbacks['task_error'].append(callback)

    def _trigger_callbacks(self, event: str, *args) -> None:
        for callback in self.callbacks[event]:
            callback(*args)
