from typing import List, Any

from intefaces.load_stategy import LoadStrategy
from intefaces.output_strategy import OutputStrategy
from intefaces.source import Source


class ListSource(Source):
    """
    列表资源类。

    该类表示以列表形式存储的数据资源，内部使用 Python 列表存储数据。

    Attributes:
        data (List[Any]): 列表数据，使用 Python 列表存储。

    Methods:
        load(strategy: LoadStrategy, source: str) -> None:
            使用指定的加载策略从源加载列表数据。

        output(strategy: OutputStrategy, target: str) -> None:
            使用指定的输出策略将列表数据输出到目标。

        get_data() -> List[Any]:
            获取列表数据的副本。

        set_data(data: List[Any]) -> None:
            设置列表数据。

        append_data(data: List[Any]) -> None:
            追加数据到列表。

        extend_data(data: List[Any]) -> None:
            扩展列表数据。

        clear_data() -> None:
            清空列表数据。

        serialize() -> List[Any]:
            将列表数据序列化为 Python 列表。

        deserialize(data: List[Any]) -> None:
            从 Python 列表反序列化列表数据。

        from_data(data: List[Any]) -> 'ListSource':
            从 Python 列表创建 ListSource 实例的替代构造器。
    """

    def __init__(self, data: List[Any] = None):
        """
        初始化 ListSource 实例。

        Args:
            data (List[Any], optional): 列表数据。默认为 None，表示创建空列表。
        """
        self.data = data if data is not None else []

    def load(self, strategy: LoadStrategy, source: str) -> None:
        """
        使用指定的加载策略从源加载列表数据。

        Args:
            strategy (LoadStrategy): 加载策略。
            source (str): 列表数据的源。

        Returns:
            None
        """
        loaded_data = strategy.load_from(source)
        self.deserialize(loaded_data)

    def output(self, strategy: OutputStrategy, target: str) -> None:
        """
        使用指定的输出策略将列表数据输出到目标。

        Args:
            strategy (OutputStrategy): 输出策略。
            target (str): 输出的目标。

        Returns:
            None
        """
        serialized_data = self.serialize()
        strategy.output_to(target, serialized_data)

    def get_data(self) -> List[Any]:
        """
        获取列表数据的副本。

        Returns:
            List[Any]: 列表数据的副本。
        """
        return self.data.copy()

    def set_data(self, data: List[Any]) -> None:
        """
        设置列表数据。

        Args:
            data (List[Any]): 要设置的列表数据。

        Returns:
            None
        """
        self.data = data.copy()

    def append_data(self, data: Any) -> None:
        """
        追加数据到列表。

        Args:
            data (Any): 要追加的数据。

        Returns:
            None
        """
        self.data.append(data)

    def extend_data(self, data: List[Any]) -> None:
        """
        扩展列表数据。

        Args:
            data (List[Any]): 要扩展的列表数据。

        Returns:
            None
        """
        self.data.extend(data)

    def clear_data(self) -> None:
        """
        清空列表数据。

        Returns:
            None
        """
        self.data.clear()

    def serialize(self) -> List[Any]:
        """
        将列表数据序列化为 Python 列表。

        Returns:
            List[Any]: 序列化后的 Python 列表。
        """
        return self.data.copy()

    def deserialize(self, data: List[Any]) -> None:
        """
        从 Python 列表反序列化列表数据。

        Args:
            data (List[Any]): 序列化的 Python 列表。

        Returns:
            None
        """
        self.data = data.copy()

    @classmethod
    def from_data(cls, data: List[Any]) -> 'ListSource':
        """
        从 Python 列表创建 ListSource 实例的替代构造器。

        Args:
            data (List[Any]): 列表数据。

        Returns:
            ListSource: 创建的 ListSource 实例。
        """
        return cls(data.copy())