from abc import ABC, abstractmethod
from typing import List, Union

from .task_interface import TaskInterface
from .config_interface import ConfigInterface


class WorkflowInterface(ABC):
    """
    工作流接口。

    工作流表示一组任务的集合，定义了任务的执行顺序和依赖关系。
    """

    @abstractmethod
    def get_name(self) -> str:
        """
        获取工作流的名称。

        Returns:
            str: 工作流的名称。
        """
        pass

    @abstractmethod
    def set_name(self, name: str) -> None:
        """
        设置工作流的名称。

        Args:
            name (str): 工作流的名称。
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """
        获取工作流的描述。

        Returns:
            str: 工作流的描述。
        """
        pass

    @abstractmethod
    def set_description(self, description: str) -> None:
        """
        设置工作流的描述。

        Args:
            description (str): 工作流的描述。
        """
        pass

    @abstractmethod
    def add_task(self, task: TaskInterface) -> None:
        """
        添加任务到工作流中。

        Args:
            task (TaskInterface): 要添加的任务。
        """
        pass

    @abstractmethod
    def remove_task(self, task: TaskInterface) -> None:
        """
        从工作流中移除任务。

        Args:
            task (TaskInterface): 要移除的任务。
        """
        pass

    @abstractmethod
    def get_tasks(self) -> List[TaskInterface]:
        """
        获取工作流中的所有任务。

        Returns:
            List[TaskInterface]: 工作流中的所有任务。
        """
        pass

    @abstractmethod
    def set_config(self, config: ConfigInterface) -> None:
        """
        设置工作流的配置。

        Args:
            config (ConfigInterface): 工作流的配置。
        """
        pass

    @abstractmethod
    def get_config(self) -> ConfigInterface:
        """
        获取工作流的配置。

        Returns:
            ConfigInterface: 工作流的配置。
        """
        pass

    @abstractmethod
    def run(self) -> None:
        """
        运行工作流。

        根据任务的执行顺序和依赖关系，依次执行工作流中的任务。
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        停止工作流的执行。

        中断当前正在执行的任务，并停止工作流的执行。
        """
        pass

    @abstractmethod
    def pause(self) -> None:
        """
        暂停工作流的执行。

        暂停当前正在执行的任务，可以通过 resume() 方法恢复执行。
        """
        pass

    @abstractmethod
    def resume(self) -> None:
        """
        恢复工作流的执行。

        恢复之前暂停的工作流执行。
        """
        pass

    @abstractmethod
    def get_status(self) -> str:
        """
        获取工作流的当前状态。

        Returns:
            str: 工作流的当前状态，可以是 "running"、"stopped"、"paused" 等。
        """
        pass

    @abstractmethod
    def on_start(self, callback: callable) -> None:
        """
        注册工作流开始执行时的回调函数。

        Args:
            callback (callable): 回调函数，当工作流开始执行时被调用。
        """
        pass

    @abstractmethod
    def on_stop(self, callback: callable) -> None:
        """
        注册工作流停止执行时的回调函数。

        Args:
            callback (callable): 回调函数，当工作流停止执行时被调用。
        """
        pass

    @abstractmethod
    def on_pause(self, callback: callable) -> None:
        """
        注册工作流暂停执行时的回调函数。

        Args:
            callback (callable): 回调函数，当工作流暂停执行时被调用。
        """
        pass

    @abstractmethod
    def on_resume(self, callback: callable) -> None:
        """
        注册工作流恢复执行时的回调函数。

        Args:
            callback (callable): 回调函数，当工作流恢复执行时被调用。
        """
        pass

    @abstractmethod
    def on_task_start(self, callback: callable) -> None:
        """
        注册任务开始执行时的回调函数。

        Args:
            callback (callable): 回调函数，当任务开始执行时被调用。
        """
        pass

    @abstractmethod
    def on_task_complete(self, callback: callable) -> None:
        """
        注册任务完成执行时的回调函数。

        Args:
            callback (callable): 回调函数，当任务完成执行时被调用。
        """
        pass

    @abstractmethod
    def on_task_error(self, callback: callable) -> None:
        """
        注册任务执行出错时的回调函数。

        Args:
            callback (callable): 回调函数，当任务执行出错时被调用。
        """
        pass