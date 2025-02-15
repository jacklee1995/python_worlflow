import csv
from typing import List

from intefaces.load_stategy import LoadStrategy


class CSVLoadStrategy(LoadStrategy):
    """
    CSV 加载策略。

    该策略用于从 CSV 文件加载数据。

    Attributes:
        delimiter (str): CSV 文件的分隔符，默认为逗号。
        quotechar (str): CSV 文件的引用字符，默认为双引号。
        encoding (str): CSV 文件的编码，默认为 UTF-8。

    Methods:
        load() -> List[List[str]]:
            从指定源加载 CSV 数据。

        set_delimiter(delimiter: str) -> None:
            设置 CSV 文件的分隔符。

        get_delimiter() -> str:
            获取 CSV 文件的分隔符。

        set_quotechar(quotechar: str) -> None:
            设置 CSV 文件的引用字符。

        get_quotechar() -> str:
            获取 CSV 文件的引用字符。

        set_encoding(encoding: str) -> None:
            设置 CSV 文件的编码。

        get_encoding() -> str:
            获取 CSV 文件的编码。
    """

    def __init__(self, source: str, delimiter: str = ',', quotechar: str = '"', encoding: str = 'utf-8'):
        """
        初始化 CSVLoadStrategy 实例。

        Args:
            source (str): CSV 文件的路径。
            delimiter (str, optional): CSV 文件的分隔符，默认为逗号。
            quotechar (str, optional): CSV 文件的引用字符，默认为双引号。
            encoding (str, optional): CSV 文件的编码，默认为 UTF-8。
        """
        super().__init__(source)
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.encoding = encoding

    def load(self) -> List[List[str]]:
        """
        从指定源加载 CSV 数据。

        Returns:
            List[List[str]]: 加载的 CSV 数据，以二维列表的形式返回。
        """
        with open(self.source, 'r', encoding=self.encoding) as file:
            reader = csv.reader(file, delimiter=self.delimiter, quotechar=self.quotechar)
            return [row for row in reader]

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

    def set_quotechar(self, quotechar: str) -> None:
        """
        设置 CSV 文件的引用字符。

        Args:
            quotechar (str): CSV 文件的引用字符。

        Returns:
            None
        """
        self.quotechar = quotechar

    def get_quotechar(self) -> str:
        """
        获取 CSV 文件的引用字符。

        Returns:
            str: CSV 文件的引用字符。
        """
        return self.quotechar

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