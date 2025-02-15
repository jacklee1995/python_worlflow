from datetime import datetime
from typing import List

from intefaces.config import Config
from intefaces.source import Source
from intefaces.task import Task


class TaskExecutor:
    """
    任务执行器。

    任务执行器负责执行任务的各个步骤，并管理任务的状态和资源。

    Attributes:
        task (Task): 要执行的任务。

    Methods:
        execute(sources: List[Source], config: Config) -> None:
            执行任务。

        set_task(task: Task) -> None:
            设置要执行的任务。

        get_task() -> Task:
            获取当前任务。
    """

    def __init__(self, task: Task):
        """
        初始化 TaskExecutor 实例。

        Args:
            task (Task): 要执行的任务。
        """
        self.task = task

    def execute(self, sources: List[Source], config: Config) -> None:
        """
        执行任务。

        Args:
            sources (List[Source]): 任务执行所需的资源列表。
            config (Config): 任务执行的配置。

        Returns:
            None
        """
        self.task.set_status("running")
        self.task.set_start_time(datetime.now())

        for step in self.task.get_steps():
            step.execute(sources, config)

        self.task.set_status("completed")
        self.task.set_end_time(datetime.now())

    def set_task(self, task: Task) -> None:
        """
        设置要执行的任务。

        Args:
            task (Task): 要执行的任务。

        Returns:
            None
        """
        self.task = task

    def get_task(self) -> Task:
        """
        获取当前任务。

        Returns:
            Task: 当前任务。
        """
        return self.task
