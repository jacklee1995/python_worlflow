import time
from typing import List

from intefaces.task import Task


class TaskMonitor:
    """
    任务监控器。

    任务监控器负责监控任务的执行状态和进度，并提供实时的监控信息。

    Attributes:
        tasks (List[Task]): 要监控的任务列表。
        monitoring_interval (int): 监控的时间间隔，单位为秒。

    Methods:
        add_task(task: Task) -> None:
            添加要监控的任务。

        remove_task(task: Task) -> None:
            移除要监控的任务。

        start_monitoring() -> None:
            开始监控任务的执行状态和进度。

        stop_monitoring() -> None:
            停止监控任务的执行状态和进度。

        _monitor_tasks() -> None:
            监控任务的执行状态和进度的内部方法。

        _display_task_status(task: Task) -> None:
            显示任务的执行状态和进度的内部方法。
    """

    def __init__(self, monitoring_interval: int = 5):
        """
        初始化 TaskMonitor 实例。

        Args:
            monitoring_interval (int): 监控的时间间隔，单位为秒，默认为 5 秒。
        """
        self.tasks: List[Task] = []
        self.monitoring_interval = monitoring_interval
        self._running = False

    def add_task(self, task: Task) -> None:
        """
        添加要监控的任务。

        Args:
            task (Task): 要监控的任务。

        Returns:
            None
        """
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """
        移除要监控的任务。

        Args:
            task (Task): 要移除的任务。

        Returns:
            None
        """
        self.tasks.remove(task)

    def start_monitoring(self) -> None:
        """
        开始监控任务的执行状态和进度。

        Returns:
            None
        """
        self._running = True
        print("Task monitoring started.")
        self._monitor_tasks()

    def stop_monitoring(self) -> None:
        """
        停止监控任务的执行状态和进度。

        Returns:
            None
        """
        self._running = False
        print("Task monitoring stopped.")

    def _monitor_tasks(self) -> None:
        """
        监控任务的执行状态和进度的内部方法。

        Returns:
            None
        """
        while self._running:
            print("\nTask Monitoring Report:")
            for task in self.tasks:
                self._display_task_status(task)
            time.sleep(self.monitoring_interval)

    def _display_task_status(self, task: Task) -> None:
        """
        显示任务的执行状态和进度的内部方法。

        Args:
            task (Task): 要显示状态的任务。

        Returns:
            None
        """
        print(f"Task Name: {task.name}")
        print(f"Status: {task.get_status()}")
        print(f"Start Time: {task.get_start_time()}")
        print(f"End Time: {task.get_end_time()}")
        print("------------------------")
