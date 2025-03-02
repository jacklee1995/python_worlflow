from abc import ABC, abstractmethod
from typing import List, Optional, AsyncIterator

from .config_interface import ConfigInterface
from .source_interface import SourceInterface
from .output_interface import OutputInterface


class StepInterface(ABC):
    """
    步骤接口。

    步骤表示任务执行过程中的一个原子操作或阶段。一个任务可以由一个或多个步骤组成。
    步骤之间通过流式管道连接，每个步骤接收上游步骤的输出流，处理后输出到下游步骤。
    """

    @abstractmethod
    def get_name(self) -> str:
        """
        获取步骤名称。

        Returns:
            str: 步骤名称。
        """
        pass

    @abstractmethod
    def set_name(self, name: str) -> None:
        """
        设置步骤名称。

        Args:
            name (str): 步骤名称。
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """
        获取步骤描述。

        Returns:
            str: 步骤描述。
        """
        pass

    @abstractmethod
    def set_description(self, description: str) -> None:
        """
        设置步骤描述。

        Args:
            description (str): 步骤描述。
        """
        pass

    @abstractmethod
    def set_config(self, config: ConfigInterface) -> None:
        """
        设置步骤的配置。

        Args:
            config (ConfigInterface): 步骤的配置。
        """
        pass

    @abstractmethod
    def get_config(self) -> ConfigInterface:
        """
        获取步骤的配置。

        Returns:
            ConfigInterface: 步骤的配置。
        """
        pass

    @abstractmethod
    def set_sources(self, sources: List[SourceInterface]) -> None:
        """
        设置步骤的数据源。

        Args:
            sources (List[SourceInterface]): 步骤的数据源列表。
        """
        pass

    @abstractmethod
    def get_sources(self) -> List[SourceInterface]:
        """
        获取步骤的数据源。

        Returns:
            List[SourceInterface]: 步骤的数据源列表。
        """
        pass

    @abstractmethod
    def set_output(self, output: OutputInterface) -> None:
        """
        设置步骤的输出目标。

        Args:
            output (OutputInterface): 步骤的输出目标。
        """
        pass

    @abstractmethod
    def get_output(self) -> OutputInterface:
        """
        获取步骤的输出目标。

        Returns:
            OutputInterface: 步骤的输出目标。
        """
        pass

    @abstractmethod
    def execute(self) -> None:
        """
        执行步骤。
        """
        pass

    @abstractmethod
    async def process(self, source: SourceInterface) -> AsyncIterator[bytes]:
        """
        处理输入流并生成输出流
        
        Args:
            source: 输入数据流
            
        Returns:
            处理后的输出数据流
        """
        pass

    @abstractmethod
    async def pipe(self, destination: 'StepInterface') -> 'StepInterface':
        """
        将当前步骤的输出连接到下一个步骤
        
        Args:
            destination: 下一个步骤
            
        Returns:
            下一个步骤实例
        """
        pass

    @abstractmethod
    async def transform(self, chunk: bytes) -> bytes:
        """
        转换数据块
        
        Args:
            chunk: 输入数据块
            
        Returns:
            转换后的数据块
        """
        pass

    @abstractmethod
    def on(self, event: str, callback: callable) -> None:
        """
        注册事件处理器
        
        Args:
            event: 事件名称
            callback: 事件处理函数
        """
        pass

    @abstractmethod 
    def off(self, event: str, callback: Optional[callable] = None) -> None:
        """
        移除事件处理器
        
        Args:
            event: 事件名称
            callback: 要移除的处理函数,为None则移除该事件所有处理器
        """
        pass