from typing import Any

from intefaces.load_stategy import LoadStrategy
from intefaces.output_strategy import OutputStrategy
from intefaces.source import Source


class StringSource(Source):
    """
    字符串资源类。

    该类表示以字符串形式存储的数据资源，内部使用 Python 字符串存储数据。

    Attributes:
        data (str): 字符串数据。

    Methods:
        load(strategy: LoadStrategy, source: str) -> None:
            使用指定的加载策略从源加载字符串数据。

        output(strategy: OutputStrategy, target: str) -> None:
            使用指定的输出策略将字符串数据输出到目标。

        get_data() -> str:
            获取字符串数据。

        set_data(data: str) -> None:
            设置字符串数据。

        append_data(data: str) -> None:
            追加数据到字符串。

        clear_data() -> None:
            清空字符串数据。

        serialize() -> str:
            将字符串数据序列化为字符串。

        deserialize(data: str) -> None:
            从字符串反序列化字符串数据。

        from_data(data: str) -> 'StringSource':
            从字符串创建 StringSource 实例的替代构造器。
    """

    def __init__(self, data: str = ""):
        """
        初始化 StringSource 实例。

        Args:
            data (str, optional): 字符串数据。默认为空字符串。
        """
        self.data = data

    def load(self, strategy: LoadStrategy, source: str) -> None:
        """
        使用指定的加载策略从源加载字符串数据。

        Args:
            strategy (LoadStrategy): 加载策略。
            source (str): 字符串数据的源。

        Returns:
            None
        """
        loaded_data = strategy.load_from(source)
        self.deserialize(loaded_data)

    def output(self, strategy: OutputStrategy, target: str) -> None:
        """
        使用指定的输出策略将字符串数据输出到目标。

        Args:
            strategy (OutputStrategy): 输出策略。
            target (str): 输出的目标。

        Returns:
            None
        """
        serialized_data = self.serialize()
        strategy.output_to(target, serialized_data)

    def get_data(self) -> str:
        """
        获取字符串数据。

        Returns:
            str: 字符串数据。
        """
        return self.data

    def set_data(self, data: str) -> None:
        """
        设置字符串数据。

        Args:
            data (str): 要设置的字符串数据。

        Returns:
            None
        """
        self.data = data

    def append_data(self, data: str) -> None:
        """
        追加数据到字符串。

        Args:
            data (str): 要追加的字符串数据。

        Returns:
            None
        """
        self.data += data

    def clear_data(self) -> None:
        """
        清空字符串数据。

        Returns:
            None
        """
        self.data = ""

    def serialize(self) -> str:
        """
        将字符串数据序列化为字符串。

        Returns:
            str: 序列化后的字符串。
        """
        return self.data

    def deserialize(self, data: str) -> None:
        """
        从字符串反序列化字符串数据。

        Args:
            data (str): 序列化的字符串。

        Returns:
            None
        """
        self.data = data

    @classmethod
    def from_data(cls, data: str) -> 'StringSource':
        """
        从字符串创建 StringSource 实例的替代构造器。

        Args:
            data (str): 字符串数据。

        Returns:
            StringSource: 创建的 StringSource 实例。
        """
        return cls(data) 