from abc import ABC, abstractmethod
from typing import List
from datetime import datetime

from intefaces.config import Config
from intefaces.source import Source
from intefaces.step import Step


class Task(ABC):
    """
    任务接口。

    任务表示一个完整的工作单元，由一个或多个步骤组成。任务基于不同的配置，以特定的方式使用资源来实现目标。

    Attributes:
        name (str): 任务名称。
        description (str): 任务描述。
        status (str): 任务状态。
        start_time (datetime): 任务开始时间。
        end_time (datetime): 任务结束时间。
        steps (List[Step]): 任务的步骤列表。

    Methods:
        execute(sources: List[Source], config: Config) -> None:
            执行任务。

        add_step(step: Step) -> None:
            添加任务步骤。

        remove_step(step: Step) -> None:
            移除任务步骤。

        set_status(status: str) -> None:
            设置任务状态。

        get_status() -> str:
            获取任务状态。

        set_start_time(start_time: datetime) -> None:
            设置任务开始时间。

        get_start_time() -> datetime:
            获取任务开始时间。

        set_end_time(end_time: datetime) -> None:
            设置任务结束时间。

        get_end_time() -> datetime:
            获取任务结束时间。

        get_steps() -> List[Step]:
            获取任务的所有步骤。
    """

    def __init__(self, name: str, description: str):
        """
        初始化任务对象。

        Args:
            name (str): 任务名称。
            description (str): 任务描述。
        """
        self.name = name
        self.description = description
        self.status = "created"
        self.start_time = None
        self.end_time = None
        self.steps = []

    @abstractmethod
    def execute(self, sources: List[Source], config: Config) -> None:
        """
        执行任务。

        Args:
            sources (List[Source]): 任务执行所需的资源列表。
            config (Config): 任务执行的配置。

        Returns:
            None
        """
        pass

    def add_step(self, step: Step) -> None:
        """
        添加任务步骤。

        Args:
            step (Step): 要添加的任务步骤。

        Returns:
            None
        """
        self.steps.append(step)

    def remove_step(self, step: Step) -> None:
        """
        移除任务步骤。

        Args:
            step (Step): 要移除的任务步骤。

        Returns:
            None
        """
        self.steps.remove(step)

    def set_status(self, status: str) -> None:
        """
        设置任务状态。

        Args:
            status (str): 任务状态。

        Returns:
            None
        """
        self.status = status

    def get_status(self) -> str:
        """
        获取任务状态。

        Returns:
            str: 任务状态。
        """
        return self.status

    def set_start_time(self, start_time: datetime) -> None:
        """
        设置任务开始时间。

        Args:
            start_time (datetime): 任务开始时间。

        Returns:
            None
        """
        self.start_time = start_time

    def get_start_time(self) -> datetime:
        """
        获取任务开始时间。

        Returns:
            datetime: 任务开始时间。
        """
        return self.start_time

    def set_end_time(self, end_time: datetime) -> None:
        """
        设置任务结束时间。

        Args:
            end_time (datetime): 任务结束时间。

        Returns:
            None
        """
        self.end_time = end_time

    def get_end_time(self) -> datetime:
        """
        获取任务结束时间。

        Returns:
            datetime: 任务结束时间。
        """
        return self.end_time

    def get_steps(self) -> List[Step]:
        """
        获取任务的所有步骤。

        Returns:
            List[Step]: 任务的所有步骤。
        """
        return self.steps