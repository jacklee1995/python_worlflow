import pandas as pd
from typing import Any

from intefaces.load_stategy import LoadStrategy
from intefaces.output_strategy import OutputStrategy
from intefaces.source import Source


class CSVSource(Source):
    """
    CSV 资源类。

    该类表示以 CSV 格式存储的数据资源，内部使用 pandas DataFrame 存储数据。

    Attributes:
        data (pd.DataFrame): CSV 数据，使用 DataFrame 存储。

    Methods:
        load(strategy: LoadStrategy, source: str) -> None:
            使用指定的加载策略从源加载 CSV 数据。

        output(strategy: OutputStrategy, target: str) -> None:
            使用指定的输出策略将 CSV 数据输出到目标。

        get_data() -> pd.DataFrame:
            获取 CSV 数据的 DataFrame。

        set_data(data: pd.DataFrame) -> None:
            设置 CSV 数据的 DataFrame。

        append_data(data: pd.DataFrame) -> None:
            追加数据到 CSV 数据的 DataFrame。

        clear_data() -> None:
            清空 CSV 数据的 DataFrame。

        serialize() -> str:
            将 CSV 数据序列化为字符串。

        deserialize(data: str) -> None:
            从字符串反序列化 CSV 数据。

        from_data(data: pd.DataFrame) -> 'CSVSource':
            从 DataFrame 创建 CSVSource 实例的替代构造器。
    """

    def __init__(self, data: pd.DataFrame = None):
        """
        初始化 CSVSource 实例。

        Args:
            data (pd.DataFrame, optional): CSV 数据的 DataFrame。默认为 None，表示创建空的 DataFrame。
        """
        self.data = data if data is not None else pd.DataFrame()

    def load(self, strategy: LoadStrategy, source: str) -> None:
        """
        使用指定的加载策略从源加载 CSV 数据。

        Args:
            strategy (LoadStrategy): 加载策略。
            source (str): CSV 数据的源。

        Returns:
            None
        """
        loaded_data = strategy.load_from(source)
        self.deserialize(loaded_data)

    def output(self, strategy: OutputStrategy, target: str) -> None:
        """
        使用指定的输出策略将 CSV 数据输出到目标。

        Args:
            strategy (OutputStrategy): 输出策略。
            target (str): 输出的目标。

        Returns:
            None
        """
        serialized_data = self.serialize()
        strategy.output_to(target, serialized_data)

    def get_data(self) -> pd.DataFrame:
        """
        获取 CSV 数据的 DataFrame。

        Returns:
            pd.DataFrame: CSV 数据的 DataFrame。
        """
        return self.data

    def set_data(self, data: pd.DataFrame) -> None:
        """
        设置 CSV 数据的 DataFrame。

        Args:
            data (pd.DataFrame): 要设置的 DataFrame 数据。

        Returns:
            None
        """
        self.data = data.copy()

    def append_data(self, data: pd.DataFrame) -> None:
        """
        追加数据到 CSV 数据的 DataFrame。

        Args:
            data (pd.DataFrame): 要追加的 DataFrame 数据。

        Returns:
            None
        """
        self.data = pd.concat([self.data, data], ignore_index=True)

    def clear_data(self) -> None:
        """
        清空 CSV 数据的 DataFrame。

        Returns:
            None
        """
        self.data = pd.DataFrame()

    def serialize(self) -> str:
        """
        将 CSV 数据序列化为字符串。

        Returns:
            str: 序列化后的 CSV 字符串。
        """
        return self.data.to_csv(index=False)

    def deserialize(self, data: str) -> None:
        """
        从字符串反序列化 CSV 数据。

        Args:
            data (str): 序列化的 CSV 字符串。

        Returns:
            None
        """
        self.data = pd.read_csv(pd.compat.StringIO(data))

    @classmethod
    def from_data(cls, data: pd.DataFrame) -> 'CSVSource':
        """
        从 DataFrame 创建 CSVSource 实例的替代构造器。

        Args:
            data (pd.DataFrame): CSV 数据的 DataFrame。

        Returns:
            CSVSource: 创建的 CSVSource 实例。
        """
        return cls(data.copy())