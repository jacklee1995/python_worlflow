from abc import ABC, abstractmethod
from typing import Any

class Config(ABC):
    """
    配置接口。

    配置表示一个任务执行所需的环境状态，用于模拟不同的环境。它为任务的执行提供必要的参数。

    Attributes:
        无

    Methods:
        get_property(key: str) -> Any:
            获取指定键的配置属性值。

        set_property(key: str, value: Any) -> None:
            设置指定键的配置属性值。

        save() -> None:
            保存配置。

        load() -> None:
            加载配置。

        to_dict() -> dict:
            将配置转换为字典。

        from_dict(data: dict) -> 'Config':
            从字典创建配置对象。
    """

    @abstractmethod
    def get_property(self, key: str) -> Any:
        """
        获取指定键的配置属性值。

        Args:
            key (str): 配置属性的键。

        Returns:
            Any: 配置属性的值。
        """
        pass

    @abstractmethod
    def set_property(self, key: str, value: Any) -> None:
        """
        设置指定键的配置属性值。

        Args:
            key (str): 配置属性的键。
            value (Any): 配置属性的值。

        Returns:
            None
        """
        pass

    @abstractmethod
    def save(self) -> None:
        """
        保存配置。

        Returns:
            None
        """
        pass

    @abstractmethod
    def load(self) -> None:
        """
        加载配置。

        Returns:
            None
        """
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """
        将配置转换为字典。

        Returns:
            dict: 表示配置的字典。
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> 'Config':
        """
        从字典创建配置对象。

        Args:
            data (dict): 包含配置数据的字典。

        Returns:
            Config: 根据字典数据创建的配置对象。
        """
        pass