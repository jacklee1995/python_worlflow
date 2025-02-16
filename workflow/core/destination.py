from typing import Any
import os
import shutil

from workflow.interfaces.destination_interface import DestinationInterface


class Destination(DestinationInterface):
    """
    目标类。

    表示数据的输出位置，可以是文件、目录、控制台等。
    """

    def __init__(self, path: str, type: str = 'file'):
        """
        初始化 Destination。

        Args:
            path (str): 目标路径。
            type (str): 目标类型，可以是 'file'、'dir'、'console' 等。
        """
        self.path = path
        self.type = type

    def write(self, data: Any) -> None:
        """
        将数据写入目标。

        Args:
            data (Any): 要写入的数据。
        """
        if self.type == 'file':
            with open(self.path, 'w') as f:
                f.write(str(data))
        elif self.type == 'dir':
            if not os.path.exists(self.path):
                os.makedirs(self.path)
        elif self.type == 'console':
            print(data)

    def exists(self) -> bool:
        """
        检查目标是否存在。

        Returns:
            bool: 如果目标存在，则返回 True，否则返回 False。
        """
        return os.path.exists(self.path)

    def remove(self) -> None:
        """
        删除目标。
        """
        if self.exists():
            if self.type == 'file':
                os.remove(self.path)
            elif self.type == 'dir':
                shutil.rmtree(self.path)

    def copy(self, dest: 'DestinationInterface') -> None:
        """
        将目标复制到另一个目标。

        Args:
            dest (DestinationInterface): 目标目标。
        """
        if self.type == 'file':
            shutil.copy(self.path, dest.get_path())
        elif self.type == 'dir':
            shutil.copytree(self.path, dest.get_path())

    def move(self, dest: 'DestinationInterface') -> None:
        """
        将目标移动到另一个目标。

        Args:
            dest (DestinationInterface): 目标目标。
        """
        shutil.move(self.path, dest.get_path())

    def rename(self, new_name: str) -> None:
        """
        重命名目标。

        Args:
            new_name (str): 新的目标名称。
        """
        new_path = os.path.join(os.path.dirname(self.path), new_name)
        os.rename(self.path, new_path)
        self.path = new_path

    def get_path(self) -> str:
        """
        获取目标的路径。

        Returns:
            str: 目标的路径。
        """
        return self.path

    def set_path(self, path: str) -> None:
        """
        设置目标的路径。

        Args:
            path (str): 目标的路径。
        """
        self.path = path

    def get_name(self) -> str:
        """
        获取目标的名称。

        Returns:
            str: 目标的名称。
        """
        return os.path.basename(self.path)

    def set_name(self, name: str) -> None:
        """
        设置目标的名称。

        Args:
            name (str): 目标的名称。
        """
        self.rename(name)

    def get_extension(self) -> str:
        """
        获取目标的扩展名。

        Returns:
            str: 目标的扩展名。
        """
        _, ext = os.path.splitext(self.path)
        return ext

    def set_extension(self, extension: str) -> None:
        """
        设置目标的扩展名。

        Args:
            extension (str): 目标的扩展名。
        """
        base, _ = os.path.splitext(self.path)
        new_path = f"{base}{extension}"
        os.rename(self.path, new_path)
        self.path = new_path
