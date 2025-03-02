from abc import ABC, abstractmethod
from typing import List, Optional, AsyncIterator, Callable

from workflow_engine.interfaces.source_interface import SourceInterface

from .task_interface import TaskInterface
from .config_interface import ConfigInterface
from .output_interface import OutputInterface


class WorkflowInterface(ABC):
    """
    工作流接口，定义工作流的基本行为。
    """

    @abstractmethod
    def get_name(self) -> str:
        """获取工作流名称"""
        pass

    @abstractmethod
    def set_name(self, name: str) -> None:
        """设置工作流名称"""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """获取工作流描述"""
        pass

    @abstractmethod
    def set_description(self, description: str) -> None:
        """设置工作流描述"""
        pass

    @abstractmethod
    async def add_task(self, task: TaskInterface) -> None:
        """添加任务到工作流"""
        pass

    @abstractmethod
    async def remove_task(self, task: TaskInterface) -> None:
        """从工作流移除任务"""
        pass

    @abstractmethod
    def get_tasks(self) -> List[TaskInterface]:
        """获取工作流中的所有任务"""
        pass

    @abstractmethod
    def set_config(self, config: ConfigInterface) -> None:
        """设置工作流配置"""
        pass

    @abstractmethod
    def get_config(self) -> Optional[ConfigInterface]:
        """获取工作流配置"""
        pass

    @abstractmethod
    def set_source(self, source: 'SourceInterface') -> None:
        """设置工作流输入源"""
        pass

    @abstractmethod
    def get_source(self) -> Optional['SourceInterface']:
        """获取工作流输入源"""
        pass

    @abstractmethod
    def set_output(self, output: OutputInterface) -> None:
        """设置工作流输出目标"""
        pass

    @abstractmethod
    def get_output(self) -> Optional[OutputInterface]:
        """获取工作流输出目标"""
        pass

    @abstractmethod
    async def execute(self) -> AsyncIterator[bytes]:
        """执行工作流"""
        pass

    @abstractmethod
    async def pipe(self, destination: 'WorkflowInterface') -> 'WorkflowInterface':
        """将工作流输出管道连接到另一个工作流"""
        pass

    @abstractmethod
    async def series(self, *tasks: TaskInterface) -> AsyncIterator[bytes]:
        """串行执行多个任务"""
        pass

    @abstractmethod
    async def parallel(self, *tasks: TaskInterface) -> List[AsyncIterator[bytes]]:
        """并行执行多个任务"""
        pass

    @abstractmethod
    def pause(self) -> None:
        """暂停工作流执行"""
        pass

    @abstractmethod
    def resume(self) -> None:
        """恢复工作流执行"""
        pass

    @abstractmethod
    def stop(self) -> None:
        """停止工作流执行"""
        pass

    @abstractmethod
    def get_status(self) -> str:
        """获取工作流状态"""
        pass

    @abstractmethod
    def on(self, event: str, callback: Callable) -> None:
        """注册事件处理器"""
        pass

    @abstractmethod
    def off(self, event: str, callback: Optional[Callable] = None) -> None:
        """移除事件处理器"""
        pass