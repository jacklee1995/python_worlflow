from abc import ABC, abstractmethod
from typing import Any


class DestinationInterface(ABC):
    """
    目标接口。

    目标表示数据的输出位置，可以是文件、目录、URL 等。
    """

    @abstractmethod
    def write(self, data: Any) -> None:
        """
        将数据写入目标。

        Args:
            data (Any): 要写入的数据。
        """
        pass

    @abstractmethod
    def exists(self) -> bool:
        """
        检查目标是否存在。

        Returns:
            bool: 如果目标存在，则返回 True，否则返回 False。
        """
        pass

    @abstractmethod
    def remove(self) -> None:
        """
        删除目标。
        """
        pass

    @abstractmethod
    def copy(self, dest: 'DestinationInterface') -> None:
        """
        将目标复制到另一个目标。

        Args:
            dest (DestinationInterface): 目标目标。
        """
        pass

    @abstractmethod
    def move(self, dest: 'DestinationInterface') -> None:
        """
        将目标移动到另一个目标。

        Args:
            dest (DestinationInterface): 目标目标。
        """
        pass

    @abstractmethod
    def rename(self, new_name: str) -> None:
        """
        重命名目标。

        Args:
            new_name (str): 新的目标名称。
        """
        pass

    @abstractmethod
    def get_path(self) -> str:
        """
        获取目标的路径。

        Returns:
            str: 目标的路径。
        """
        pass

    @abstractmethod
    def set_path(self, path: str) -> None:
        """
        设置目标的路径。

        Args:
            path (str): 目标的路径。
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """
        获取目标的名称。

        Returns:
            str: 目标的名称。
        """
        pass

    @abstractmethod
    def set_name(self, name: str) -> None:
        """
        设置目标的名称。

        Args:
            name (str): 目标的名称。
        """
        pass

    @abstractmethod
    def get_extension(self) -> str:
        """
        获取目标的扩展名。

        Returns:
            str: 目标的扩展名。
        """
        pass

    @abstractmethod
    def set_extension(self, extension: str) -> None:
        """
        设置目标的扩展名。

        Args:
            extension (str): 目标的扩展名。
        """
        pass