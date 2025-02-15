import time
from typing import List
from datetime import datetime, timedelta

from intefaces.config import Config
from intefaces.source import Source
from intefaces.task import Task
from task.task_manager import TaskManager


class TaskScheduler:
    """
    任务调度器。

    任务调度器负责调度任务的执行时间和频率，可以设置任务的开始时间、结束时间和执行间隔。

    Attributes:
        task_manager (TaskManager): 任务管理器，用于管理和执行任务。
        start_time (datetime): 任务调度的开始时间。
        end_time (datetime): 任务调度的结束时间。
        interval (timedelta): 任务执行的时间间隔。

    Methods:
        set_task_manager(task_manager: TaskManager) -> None:
            设置任务管理器。

        set_start_time(start_time: datetime) -> None:
            设置任务调度的开始时间。

        set_end_time(end_time: datetime) -> None:
            设置任务调度的结束时间。

        set_interval(interval: timedelta) -> None:
            设置任务执行的时间间隔。

        schedule(sources: List[Source], config: Config) -> None:
            调度任务的执行。

        stop() -> None:
            停止任务调度。
    """

    def __init__(self, task_manager: TaskManager):
        """
        初始化 TaskScheduler 实例。

        Args:
            task_manager (TaskManager): 任务管理器，用于管理和执行任务。
        """
        self.task_manager = task_manager
        self.start_time = datetime.now()
        self.end_time = None
        self.interval = timedelta(minutes=1)
        self._running = False

    def set_task_manager(self, task_manager: TaskManager) -> None:
        """
        设置任务管理器。

        Args:
            task_manager (TaskManager): 任务管理器，用于管理和执行任务。

        Returns:
            None
        """
        self.task_manager = task_manager

    def set_start_time(self, start_time: datetime) -> None:
        """
        设置任务调度的开始时间。

        Args:
            start_time (datetime): 任务调度的开始时间。

        Returns:
            None
        """
        self.start_time = start_time

    def set_end_time(self, end_time: datetime) -> None:
        """
        设置任务调度的结束时间。

        Args:
            end_time (datetime): 任务调度的结束时间。

        Returns:
            None
        """
        self.end_time = end_time

    def set_interval(self, interval: timedelta) -> None:
        """
        设置任务执行的时间间隔。

        Args:
            interval (timedelta): 任务执行的时间间隔。

        Returns:
            None
        """
        self.interval = interval

    def schedule(self, sources: List[Source], config: Config) -> None:
        """
        调度任务的执行。

        Args:
            sources (List[Source]): 任务执行所需的资源列表。
            config (Config): 任务执行的配置。

        Returns:
            None
        """
        self._running = True
        next_run_time = self.start_time

        while self._running:
            current_time = datetime.now()

            if current_time >= next_run_time:
                self.task_manager.execute_tasks_async(sources, config)
                next_run_time += self.interval

            if self.end_time and current_time >= self.end_time:
                self._running = False

            time.sleep(1)

    def stop(self) -> None:
        """
        停止任务调度。

        Returns:
            None
        """
        self._running = False
        self.task_manager.shutdown()
