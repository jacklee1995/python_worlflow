from typing import List

from intefaces.step import Step
from intefaces.task import Task


class TaskBuilder:
    """
    任务构建器。

    任务构建器用于创建和配置任务，可以添加多个步骤来构建任务。

    Attributes:
        task (Task): 正在构建的任务。

    Methods:
        set_name(name: str) -> 'TaskBuilder':
            设置任务名称。

        set_description(description: str) -> 'TaskBuilder':
            设置任务描述。

        add_step(step: Step) -> 'TaskBuilder':
            添加任务步骤。

        remove_step(step: Step) -> 'TaskBuilder':
            移除任务步骤。

        get_steps() -> List[Step]:
            获取任务的所有步骤。

        build() -> Task:
            构建并返回配置好的任务。
    """

    def __init__(self, name: str, description: str):
        """
        初始化 TaskBuilder 实例。

        Args:
            name (str): 任务名称。
            description (str): 任务描述。
        """
        self.task = Task(name, description)

    def set_name(self, name: str) -> 'TaskBuilder':
        """
        设置任务名称。

        Args:
            name (str): 任务名称。

        Returns:
            TaskBuilder: 当前的 TaskBuilder 实例。
        """
        self.task.name = name
        return self

    def set_description(self, description: str) -> 'TaskBuilder':
        """
        设置任务描述。

        Args:
            description (str): 任务描述。

        Returns:
            TaskBuilder: 当前的 TaskBuilder 实例。
        """
        self.task.description = description
        return self

    def add_step(self, step: Step) -> 'TaskBuilder':
        """
        添加任务步骤。

        Args:
            step (Step): 要添加的任务步骤。

        Returns:
            TaskBuilder: 当前的 TaskBuilder 实例。
        """
        self.task.add_step(step)
        return self

    def remove_step(self, step: Step) -> 'TaskBuilder':
        """
        移除任务步骤。

        Args:
            step (Step): 要移除的任务步骤。

        Returns:
            TaskBuilder: 当前的 TaskBuilder 实例。
        """
        self.task.remove_step(step)
        return self

    def get_steps(self) -> List[Step]:
        """
        获取任务的所有步骤。

        Returns:
            List[Step]: 任务的所有步骤。
        """
        return self.task.get_steps()

    def build(self) -> Task:
        """
        构建并返回配置好的任务。

        Returns:
            Task: 配置好的任务。
        """
        return self.task
