from typing import Dict, Type, Optional, Any
import asyncio

from workflow_engine.interfaces.workflow_interface import WorkflowInterface
from workflow_engine.interfaces.source_interface import SourceInterface
from workflow_engine.interfaces.output_interface import OutputInterface


class WorkflowRegistry:
    """
    工作流注册表，用于注册和管理所有的工作流。
    """
    _workflows: Dict[str, Type[WorkflowInterface]] = {}
    _instances: Dict[str, WorkflowInterface] = {}
    _event_handlers = {
        'register': [],
        'unregister': [],
        'create': [],
        'destroy': []
    }

    @classmethod
    def register(cls, name: str, workflow_class: Type[WorkflowInterface]) -> None:
        """
        注册工作流类。

        Args:
            name: 工作流名称
            workflow_class: 工作流类
        """
        if name in cls._workflows:
            raise ValueError(f"Workflow '{name}' already registered")
        
        cls._workflows[name] = workflow_class
        for handler in cls._event_handlers['register']:
            handler(name, workflow_class)

    @classmethod
    def unregister(cls, name: str) -> None:
        """
        取消注册工作流类。

        Args:
            name: 工作流名称
        """
        if name not in cls._workflows:
            raise ValueError(f"Workflow '{name}' not found")
        
        workflow_class = cls._workflows.pop(name)
        for handler in cls._event_handlers['unregister']:
            handler(name, workflow_class)

    @classmethod
    def get(cls, name: str) -> Optional[Type[WorkflowInterface]]:
        """
        获取工作流类。

        Args:
            name: 工作流名称

        Returns:
            工作流类，如果不存在则返回 None
        """
        return cls._workflows.get(name)

    @classmethod
    async def create(
        cls, 
        name: str, 
        source: Optional[SourceInterface] = None,
        output: Optional[OutputInterface] = None,
        **kwargs: Any
    ) -> WorkflowInterface:
        """
        创建工作流实例。

        Args:
            name: 工作流名称
            source: 输入数据源
            output: 输出目标
            **kwargs: 工作流初始化参数

        Returns:
            工作流实例

        Raises:
            ValueError: 工作流未注册
        """
        workflow_class = cls.get(name)
        if not workflow_class:
            raise ValueError(f"Workflow '{name}' not found")

        instance = workflow_class(**kwargs)
        if source:
            instance.set_source(source)
        if output:
            instance.set_output(output)

        cls._instances[name] = instance
        for handler in cls._event_handlers['create']:
            handler(name, instance)

        return instance

    @classmethod
    async def destroy(cls, name: str) -> None:
        """
        销毁工作流实例。

        Args:
            name: 工作流名称

        Raises:
            ValueError: 工作流实例不存在
        """
        if name not in cls._instances:
            raise ValueError(f"Workflow instance '{name}' not found")

        instance = cls._instances.pop(name)
        instance.stop()
        for handler in cls._event_handlers['destroy']:
            handler(name, instance)

    @classmethod
    def get_instance(cls, name: str) -> Optional[WorkflowInterface]:
        """
        获取工作流实例。

        Args:
            name: 工作流名称

        Returns:
            工作流实例，如果不存在则返回 None
        """
        return cls._instances.get(name)

    @classmethod
    def get_all_instances(cls) -> Dict[str, WorkflowInterface]:
        """
        获取所有工作流实例。

        Returns:
            工作流实例字典，键为工作流名称，值为工作流实例
        """
        return cls._instances.copy()

    @classmethod
    def on(cls, event: str, callback: callable) -> None:
        """
        注册事件处理器。

        Args:
            event: 事件名称
            callback: 事件处理函数
        """
        if event not in cls._event_handlers:
            raise ValueError(f"Unsupported event: {event}")
        cls._event_handlers[event].append(callback)

    @classmethod
    def off(cls, event: str, callback: Optional[callable] = None) -> None:
        """
        移除事件处理器。

        Args:
            event: 事件名称
            callback: 要移除的处理函数，为 None 则移除该事件所有处理器
        """
        if event not in cls._event_handlers:
            raise ValueError(f"Unsupported event: {event}")
        if callback is None:
            cls._event_handlers[event].clear()
        else:
            cls._event_handlers[event] = [
                h for h in cls._event_handlers[event] if h != callback
            ] 