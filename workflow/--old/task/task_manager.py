from typing import List
from concurrent.futures import ThreadPoolExecutor

from intefaces.config import Config
from intefaces.source import Source
from intefaces.task import Task
from task.task_executor import TaskExecutor


class TaskManager:
    """
    任务管理器。

    任务管理器负责管理和调度任务的执行，可以同步或异步执行多个任务。

    Attributes:
        tasks (List[Task]): 任务列表。
        executor (ThreadPoolExecutor): 线程池执行器，用于异步执行任务。

    Methods:
        add_task(task: Task) -> None:
            添加任务到任务列表。

        remove_task(task: Task) -> None:
            从任务列表中移除任务。

        get_tasks() -> List[Task]:
            获取所有任务。

        execute_tasks(sources: List[Source], config: Config) -> None:
            同步执行任务列表中的所有任务。

        execute_tasks_async(sources: List[Source], config: Config) -> None:
            异步执行任务列表中的所有任务。

        shutdown() -> None:
            关闭任务管理器，等待所有任务完成。
    """

    def __init__(self):
        """
        初始化 TaskManager 实例。
        """
        self.tasks: List[Task] = []
        self.executor = ThreadPoolExecutor()

    def add_task(self, task: Task) -> None:
        """
        添加任务到任务列表。

        Args:
            task (Task): 要添加的任务。

        Returns:
            None
        """
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """
        从任务列表中移除任务。

        Args:
            task (Task): 要移除的任务。

        Returns:
            None
        """
        self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """
        获取所有任务。

        Returns:
            List[Task]: 任务列表。
        """
        return self.tasks

    def execute_tasks(self, sources: List[Source], config: Config) -> None:
        """
        同步执行任务列表中的所有任务。

        Args:
            sources (List[Source]): 任务执行所需的资源列表。
            config (Config): 任务执行的配置。

        Returns:
            None
        """
        for task in self.tasks:
            executor = TaskExecutor(task)
            executor.execute(sources, config)

    def execute_tasks_async(self, sources: List[Source], config: Config) -> None:
        """
        异步执行任务列表中的所有任务。

        Args:
            sources (List[Source]): 任务执行所需的资源列表。
            config (Config): 任务执行的配置。

        Returns:
            None
        """
        futures = []
        for task in self.tasks:
            executor = TaskExecutor(task)
            future = self.executor.submit(executor.execute, sources, config)
            futures.append(future)

        for future in futures:
            future.result()

    def shutdown(self) -> None:
        """
        关闭任务管理器，等待所有任务完成。

        Returns:
            None
        """
        self.executor.shutdown(wait=True)
