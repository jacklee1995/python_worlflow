import pandas as pd

from intefaces.load_stategy import LoadStrategy
from sources.dataframe_source import DataFrameSource


class TextToDataFrameLoadStrategy(LoadStrategy):
    """
    文本转 DataFrame 加载策略。

    该策略用于将特定格式的文本文件加载为 DataFrameSource。

    Attributes:
        delimiter (str): 文本文件的分隔符，默认为空格。
        header (int): 文本文件的表头行索引，默认为 None，表示没有表头行。

    Methods:
        load() -> DataFrameSource:
            从指定源加载文本数据，并转换为 DataFrameSource。

        set_delimiter(delimiter: str) -> None:
            设置文本文件的分隔符。

        get_delimiter() -> str:
            获取文本文件的分隔符。

        set_header(header: int) -> None:
            设置文本文件的表头行索引。

        get_header() -> int:
            获取文本文件的表头行索引。
    """

    def __init__(self, source: str, delimiter: str = ' ', header: int = None):
        """
        初始化 TextToDataFrameLoadStrategy 实例。

        Args:
            source (str): 文本文件的路径。
            delimiter (str, optional): 文本文件的分隔符，默认为空格。
            header (int, optional): 文本文件的表头行索引，默认为 None，表示没有表头行。
        """
        super().__init__(source)
        self.delimiter = delimiter
        self.header = header

    def load(self) -> DataFrameSource:
        """
        从指定源加载文本数据，并转换为 DataFrameSource。

        Returns:
            DataFrameSource: 加载并转换后的 DataFrameSource 对象。
        """
        df = pd.read_csv(self.source, delimiter=self.delimiter, header=self.header)
        return DataFrameSource(df)

    def set_delimiter(self, delimiter: str) -> None:
        """
        设置文本文件的分隔符。

        Args:
            delimiter (str): 文本文件的分隔符。

        Returns:
            None
        """
        self.delimiter = delimiter

    def get_delimiter(self) -> str:
        """
        获取文本文件的分隔符。

        Returns:
            str: 文本文件的分隔符。
        """
        return self.delimiter

    def set_header(self, header: int) -> None:
        """
        设置文本文件的表头行索引。

        Args:
            header (int): 文本文件的表头行索引。

        Returns:
            None
        """
        self.header = header

    def get_header(self) -> int:
        """
        获取文本文件的表头行索引。

        Returns:
            int: 文本文件的表头行索引。
        """
        return self.header 