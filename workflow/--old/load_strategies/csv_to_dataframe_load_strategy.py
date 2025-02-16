import pandas as pd

from intefaces.load_stategy import LoadStrategy
from sources.dataframe_source import DataFrameSource


class CSVToDataFrameLoadStrategy(LoadStrategy):
    """
    CSV 转 DataFrame 加载策略。

    该策略用于将 CSV 文件加载为 DataFrameSource。

    Attributes:
        delimiter (str): CSV 文件的分隔符，默认为逗号。
        header (int): CSV 文件的表头行索引，默认为 0，表示第一行为表头。
        encoding (str): CSV 文件的编码，默认为 UTF-8。

    Methods:
        load() -> DataFrameSource:
            从指定源加载 CSV 数据，并转换为 DataFrameSource。

        set_delimiter(delimiter: str) -> None:
            设置 CSV 文件的分隔符。

        get_delimiter() -> str:
            获取 CSV 文件的分隔符。

        set_header(header: int) -> None:
            设置 CSV 文件的表头行索引。

        get_header() -> int:
            获取 CSV 文件的表头行索引。

        set_encoding(encoding: str) -> None:
            设置 CSV 文件的编码。

        get_encoding() -> str:
            获取 CSV 文件的编码。
    """

    def __init__(self, source: str, delimiter: str = ',', header: int = 0, encoding: str = 'utf-8'):
        """
        初始化 CSVToDataFrameLoadStrategy 实例。

        Args:
            source (str): CSV 文件的路径。
            delimiter (str, optional): CSV 文件的分隔符，默认为逗号。
            header (int, optional): CSV 文件的表头行索引，默认为 0，表示第一行为表头。
            encoding (str, optional): CSV 文件的编码，默认为 UTF-8。
        """
        super().__init__(source)
        self.delimiter = delimiter
        self.header = header
        self.encoding = encoding

    def load(self) -> DataFrameSource:
        """
        从指定源加载 CSV 数据，并转换为 DataFrameSource。

        Returns:
            DataFrameSource: 加载并转换后的 DataFrameSource 对象。
        """
        df = pd.read_csv(self.source, delimiter=self.delimiter, header=self.header, encoding=self.encoding)
        return DataFrameSource(df)

    def set_delimiter(self, delimiter: str) -> None:
        """
        设置 CSV 文件的分隔符。

        Args:
            delimiter (str): CSV 文件的分隔符。

        Returns:
            None
        """
        self.delimiter = delimiter

    def get_delimiter(self) -> str:
        """
        获取 CSV 文件的分隔符。

        Returns:
            str: CSV 文件的分隔符。
        """
        return self.delimiter

    def set_header(self, header: int) -> None:
        """
        设置 CSV 文件的表头行索引。

        Args:
            header (int): CSV 文件的表头行索引。

        Returns:
            None
        """
        self.header = header

    def get_header(self) -> int:
        """
        获取 CSV 文件的表头行索引。

        Returns:
            int: CSV 文件的表头行索引。
        """
        return self.header

    def set_encoding(self, encoding: str) -> None:
        """
        设置 CSV 文件的编码。

        Args:
            encoding (str): CSV 文件的编码。

        Returns:
            None
        """
        self.encoding = encoding

    def get_encoding(self) -> str:
        """
        获取 CSV 文件的编码。

        Returns:
            str: CSV 文件的编码。
        """
        return self.encoding 