from abc import ABC, abstractmethod
from typing import List, Optional, AsyncIterator, Callable

from .step_interface import StepInterface
from .config_interface import ConfigInterface
from .source_interface import SourceInterface
from .output_interface import OutputInterface


class TaskInterface(ABC):
    """
    任务接口。

    任务表示一个完整的工作单元，由一个或多个步骤组成。任务可以串行或并行执行。
    每个任务都是一个异步数据流处理管道,通过步骤之间的pipe连接形成处理链。
    """

    @abstractmethod
    def get_name(self) -> str:
        """获取任务名称"""
        pass

    @abstractmethod
    def set_name(self, name: str) -> None:
        """设置任务名称"""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """获取任务描述"""
        pass

    @abstractmethod
    def set_description(self, description: str) -> None:
        """设置任务描述"""
        pass

    @abstractmethod
    async def add_step(self, step: StepInterface) -> None:
        """添加处理步骤到任务管道"""
        pass

    @abstractmethod
    async def remove_step(self, step: StepInterface) -> None:
        """从任务管道移除处理步骤"""
        pass

    @abstractmethod
    def get_steps(self) -> List[StepInterface]:
        """获取任务管道中的所有处理步骤"""
        pass

    @abstractmethod
    async def execute(self) -> AsyncIterator[bytes]:
        """
        执行任务管道处理

        Returns:
            处理后的输出数据流
        """
        pass

    @abstractmethod
    async def pipe(self, destination: 'TaskInterface') -> 'TaskInterface':
        """
        将当前任务的输出连接到下一个任务

        Args:
            destination: 下一个任务

        Returns:
            下一个任务实例
        """
        pass

    @abstractmethod
    async def series(self, *steps: StepInterface) -> AsyncIterator[bytes]:
        """
        串行执行多个处理步骤
        
        Args:
            steps: 要串行执行的步骤列表
            
        Returns:
            处理后的输出数据流
        """
        pass

    @abstractmethod
    async def parallel(self, *steps: StepInterface) -> List[AsyncIterator[bytes]]:
        """
        并行执行多个处理步骤
        
        Args:
            steps: 要并行执行的步骤列表
            
        Returns:
            多个处理后的输出数据流列表
        """
        pass

    @abstractmethod
    def set_config(self, config: ConfigInterface) -> None:
        """设置任务配置"""
        pass

    @abstractmethod
    def get_config(self) -> Optional[ConfigInterface]:
        """获取任务配置"""
        pass

    @abstractmethod
    def set_source(self, source: SourceInterface) -> None:
        """设置任务输入源"""
        pass

    @abstractmethod
    def get_source(self) -> Optional[SourceInterface]:
        """获取任务输入源"""
        pass

    @abstractmethod
    def set_output(self, output: OutputInterface) -> None:
        """设置任务输出目标"""
        pass

    @abstractmethod
    def get_output(self) -> Optional[OutputInterface]:
        """获取任务输出目标"""
        pass

    @abstractmethod
    def on(self, event: str, callback: Callable) -> None:
        """
        注册事件处理器
        
        Args:
            event: 事件名称
            callback: 事件处理函数
        """
        pass

    @abstractmethod
    def off(self, event: str, callback: Optional[Callable] = None) -> None:
        """
        移除事件处理器
        
        Args:
            event: 事件名称
            callback: 要移除的处理函数,为None则移除该事件所有处理器
        """
        pass

    @abstractmethod
    def pause(self) -> None:
        """暂停任务执行"""
        pass

    @abstractmethod
    def resume(self) -> None:
        """恢复任务执行"""
        pass

    @abstractmethod
    def stop(self) -> None:
        """停止任务执行"""
        pass

    @abstractmethod
    def get_status(self) -> str:
        """获取任务状态"""
        pass