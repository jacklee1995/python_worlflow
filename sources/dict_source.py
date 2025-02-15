from typing import Any, Dict

from intefaces.load_stategy import LoadStrategy
from intefaces.output_strategy import OutputStrategy
from intefaces.source import Source


class DictSource(Source):
    """
    字典资源类。

    该类表示以字典形式存储的数据资源，内部使用 Python 字典存储数据。

    Attributes:
        data (Dict[str, Any]): 字典数据，使用 Python 字典存储。

    Methods:
        load(strategy: LoadStrategy, source: str) -> None:
            使用指定的加载策略从源加载字典数据。

        output(strategy: OutputStrategy, target: str) -> None:
            使用指定的输出策略将字典数据输出到目标。

        get_data() -> Dict[str, Any]:
            获取字典数据的副本。

        set_data(data: Dict[str, Any]) -> None:
            设置字典数据。

        update_data(data: Dict[str, Any]) -> None:
            使用新的字典更新字典数据。

        clear_data() -> None:
            清空字典数据。

        serialize() -> Dict[str, Any]:
            将字典数据序列化为 Python 字典。

        deserialize(data: Dict[str, Any]) -> None:
            从 Python 字典反序列化字典数据。

        from_data(data: Dict[str, Any]) -> 'DictSource':
            从 Python 字典创建 DictSource 实例的替代构造器。
    """

    def __init__(self, data: Dict[str, Any] = None):
        """
        初始化 DictSource 实例。

        Args:
            data (Dict[str, Any], optional): 字典数据。默认为 None，表示创建空字典。
        """
        self.data = data if data is not None else {}

    def load(self, strategy: LoadStrategy, source: str) -> None:
        """
        使用指定的加载策略从源加载字典数据。

        Args:
            strategy (LoadStrategy): 加载策略。
            source (str): 字典数据的源。

        Returns:
            None
        """
        loaded_data = strategy.load()
        self.deserialize(loaded_data)

    def output(self, strategy: OutputStrategy, target: str) -> None:
        """
        使用指定的输出策略将字典数据输出到目标。

        Args:
            strategy (OutputStrategy): 输出策略。
            target (str): 输出的目标。

        Returns:
            None
        """
        serialized_data = self.serialize()
        strategy.output(serialized_data)

    def get_data(self) -> Dict[str, Any]:
        """
        获取字典数据的副本。

        Returns:
            Dict[str, Any]: 字典数据的副本。
        """
        return self.data.copy()

    def set_data(self, data: Dict[str, Any]) -> None:
        """
        设置字典数据。

        Args:
            data (Dict[str, Any]): 要设置的字典数据。

        Returns:
            None
        """
        self.data = data.copy()

    def update_data(self, data: Dict[str, Any]) -> None:
        """
        使用新的字典更新字典数据。

        Args:
            data (Dict[str, Any]): 要更新的字典数据。

        Returns:
            None
        """
        self.data.update(data)

    def clear_data(self) -> None:
        """
        清空字典数据。

        Returns:
            None
        """
        self.data.clear()

    def serialize(self) -> Dict[str, Any]:
        """
        将字典数据序列化为 Python 字典。

        Returns:
            Dict[str, Any]: 序列化后的 Python 字典。
        """
        return self.data.copy()

    def deserialize(self, data: Dict[str, Any]) -> None:
        """
        从 Python 字典反序列化字典数据。

        Args:
            data (Dict[str, Any]): 序列化的 Python 字典。

        Returns:
            None
        """
        self.data = data.copy()

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> 'DictSource':
        """
        从 Python 字典创建 DictSource 实例的替代构造器。

        Args:
            data (Dict[str, Any]): 字典数据。

        Returns:
            DictSource: 创建的 DictSource 实例。
        """
        return cls(data.copy())
