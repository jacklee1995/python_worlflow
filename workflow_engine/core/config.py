import os
from typing import Any, Dict

from workflow_engine.interfaces.config_interface import ConfigInterface


class Config(ConfigInterface):
    """
    配置类。

    用于管理任务运行的可选参数，支持从不同来源加载配置。
    """

    def __init__(self, data: Dict[str, Any] = None, base_dir: str = '.'):
        """
        初始化 Config。

        Args:
            data (Dict[str, Any]): 初始配置数据。
            base_dir (str): 基础目录,默认为当前目录。
        """
        self.data = data or {}
        self.base_dir = base_dir

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取指定键的配置值。

        Args:
            key (str): 配置键。
            default (Any): 默认值，当键不存在时返回。

        Returns:
            Any: 配置值，如果键不存在，则返回默认值。
        """
        value = self.data.get(key, default)
        if isinstance(value, str):
            value = self._resolve_path(value)
        return value

    def set(self, key: str, value: Any) -> None:
        """
        设置指定键的配置值。

        Args:
            key (str): 配置键。
            value (Any): 配置值。
        """
        self.data[key] = value

    def has(self, key: str) -> bool:
        """
        检查是否存在指定键的配置。

        Args:
            key (str): 配置键。

        Returns:
            bool: 如果存在指定键的配置，则返回 True，否则返回 False。
        """
        return key in self.data

    def remove(self, key: str) -> None:
        """
        移除指定键的配置。

        Args:
            key (str): 配置键。
        """
        if self.has(key):
            del self.data[key]

    def clear(self) -> None:
        """
        清空所有配置。
        """
        self.data.clear()

    def to_dict(self) -> Dict[str, Any]:
        """
        将配置转换为字典。

        Returns:
            Dict[str, Any]: 包含所有配置的字典。
        """
        return self.data.copy()

    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        从字典中加载配置。

        Args:
            data (Dict[str, Any]): 包含配置的字典。
        """
        self.data.update(data)

    def load(self) -> None:
        """
        加载配置。

        根据配置加载器的实现，从指定的源（如配置文件、环境变量、配置中心等）加载配置。
        """
        # 在子类中实现具体的加载逻辑
        pass

    def save(self) -> None:
        """
        保存配置。

        根据配置加载器的实现，将配置保存到指定的目标（如配置文件、配置中心等）。
        """
        # 在子类中实现具体的保存逻辑
        pass

    def reload(self) -> None:
        """
        重新加载配置。

        当配置发生变化时，重新加载配置。这可能会触发相关的任务重新执行。
        """
        self.clear()
        self.load()

    def _resolve_path(self, path: str) -> str:
        """
        将相对路径转换为绝对路径。

        Args:
            path (str): 文件路径。

        Returns:
            str: 转换后的绝对路径。
        """
        if not os.path.isabs(path):
            path = os.path.join(self.base_dir, path)
        return os.path.abspath(path)
