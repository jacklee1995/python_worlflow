import pandas as pd
from typing import Any

from intefaces.load_stategy import LoadStrategy
from intefaces.output_strategy import OutputStrategy
from intefaces.source import Source


class XlsSource(Source):
    """
    XLS 资源类。

    该类表示以 XLS 格式存储的数据资源，内部使用 pandas DataFrame 存储数据。

    Attributes:
        data (pd.DataFrame): XLS 数据，使用 DataFrame 存储。

    Methods:
        load(strategy: LoadStrategy, source: str) -> None:
            使用指定的加载策略从源加载 XLS 数据。

        output(strategy: OutputStrategy, target: str) -> None:
            使用指定的输出策略将 XLS 数据输出到目标。

        get_data() -> pd.DataFrame:
            获取 XLS 数据的 DataFrame。

        set_data(data: pd.DataFrame) -> None:
            设置 XLS 数据的 DataFrame。

        append_data(data: pd.DataFrame) -> None:
            追加数据到 XLS 数据的 DataFrame。

        clear_data() -> None:
            清空 XLS 数据的 DataFrame。

        serialize() -> bytes:
            将 XLS 数据序列化为字节流。

        deserialize(data: bytes) -> None:
            从字节流反序列化 XLS 数据。

        from_data(data: pd.DataFrame) -> 'XlsSource':
            从 DataFrame 创建 XlsSource 实例的替代构造器。
    """

    def __init__(self, data: pd.DataFrame = None):
        """
        初始化 XlsSource 实例。

        Args:
            data (pd.DataFrame, optional): XLS 数据的 DataFrame。默认为 None，表示创建空的 DataFrame。
        """
        self.data = data if data is not None else pd.DataFrame()

    def load(self, strategy: LoadStrategy, source: str) -> None:
        """
        使用指定的加载策略从源加载 XLS 数据。

        Args:
            strategy (LoadStrategy): 加载策略。
            source (str): XLS 数据的源。

        Returns:
            None
        """
        loaded_data = strategy.load_from(source)
        self.deserialize(loaded_data)

    def output(self, strategy: OutputStrategy, target: str) -> None:
        """
        使用指定的输出策略将 XLS 数据输出到目标。

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
        获取 XLS 数据的 DataFrame。

        Returns:
            pd.DataFrame: XLS 数据的 DataFrame。
        """
        return self.data

    def set_data(self, data: pd.DataFrame) -> None:
        """
        设置 XLS 数据的 DataFrame。

        Args:
            data (pd.DataFrame): 要设置的 DataFrame 数据。

        Returns:
            None
        """
        self.data = data.copy()

    def append_data(self, data: pd.DataFrame) -> None:
        """
        追加数据到 XLS 数据的 DataFrame。

        Args:
            data (pd.DataFrame): 要追加的 DataFrame 数据。

        Returns:
            None
        """
        self.data = pd.concat([self.data, data], ignore_index=True)

    def clear_data(self) -> None:
        """
        清空 XLS 数据的 DataFrame。

        Returns:
            None
        """
        self.data = pd.DataFrame()

    def serialize(self) -> bytes:
        """
        将 XLS 数据序列化为字节流。

        Returns:
            bytes: 序列化后的 XLS 字节流。
        """
        with pd.ExcelWriter("temp.xls", engine="xlwt") as writer:
            self.data.to_excel(writer, index=False)
        with open("temp.xls", "rb") as f:
            return f.read()

    def deserialize(self, data: bytes) -> None:
        """
        从字节流反序列化 XLS 数据。

        Args:
            data (bytes): 序列化的 XLS 字节流。

        Returns:
            None
        """
        with open("temp.xls", "wb") as f:
            f.write(data)
        self.data = pd.read_excel("temp.xls")

    @classmethod
    def from_data(cls, data: pd.DataFrame) -> 'XlsSource':
        """
        从 DataFrame 创建 XlsSource 实例的替代构造器。

        Args:
            data (pd.DataFrame): XLS 数据的 DataFrame。

        Returns:
            XlsSource: 创建的 XlsSource 实例。
        """
        return cls(data.copy())