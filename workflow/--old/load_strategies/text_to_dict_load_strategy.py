from typing import Dict

from intefaces.load_stategy import LoadStrategy
from sources.dict_source import DictSource


class TextToDictLoadStrategy(LoadStrategy):
    """
    文本转 Dict 加载策略。

    该策略用于将特定格式的文本文件加载为 DictSource。

    Attributes:
        delimiter (str): 文本文件的分隔符，默认为空格。
        key_index (int): 文本文件中作为键的列索引，默认为 0。
        value_index (int): 文本文件中作为值的列索引，默认为 1。

    Methods:
        load() -> DictSource:
            从指定源加载文本数据，并转换为 DictSource。

        set_delimiter(delimiter: str) -> None:
            设置文本文件的分隔符。

        get_delimiter() -> str:
            获取文本文件的分隔符。

        set_key_index(key_index: int) -> None:
            设置文本文件中作为键的列索引。

        get_key_index() -> int:
            获取文本文件中作为键的列索引。

        set_value_index(value_index: int) -> None:
            设置文本文件中作为值的列索引。

        get_value_index() -> int:
            获取文本文件中作为值的列索引。
    """

    def __init__(self, source: str, delimiter: str = ' ', key_index: int = 0, value_index: int = 1):
        """
        初始化 TextToDictLoadStrategy 实例。

        Args:
            source (str): 文本文件的路径。
            delimiter (str, optional): 文本文件的分隔符，默认为空格。
            key_index (int, optional): 文本文件中作为键的列索引，默认为 0。
            value_index (int, optional): 文本文件中作为值的列索引，默认为 1。
        """
        super().__init__(source)
        self.delimiter = delimiter
        self.key_index = key_index
        self.value_index = value_index

    def load(self) -> DictSource:
        """
        从指定源加载文本数据，并转换为 DictSource。

        Returns:
            DictSource: 加载并转换后的 DictSource 对象。
        """
        data: Dict[str, str] = {}
        with open(self.source, 'r') as file:
            for line in file:
                fields = line.strip().split(self.delimiter)
                if len(fields) > max(self.key_index, self.value_index):
                    key = fields[self.key_index]
                    value = fields[self.value_index]
                    data[key] = value
        return DictSource(data)

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

    def set_key_index(self, key_index: int) -> None:
        """
        设置文本文件中作为键的列索引。

        Args:
            key_index (int): 文本文件中作为键的列索引。

        Returns:
            None
        """
        self.key_index = key_index

    def get_key_index(self) -> int:
        """
        获取文本文件中作为键的列索引。

        Returns:
            int: 文本文件中作为键的列索引。
        """
        return self.key_index

    def set_value_index(self, value_index: int) -> None:
        """
        设置文本文件中作为值的列索引。

        Args:
            value_index (int): 文本文件中作为值的列索引。

        Returns:
            None
        """
        self.value_index = value_index

    def get_value_index(self) -> int:
        """
        获取文本文件中作为值的列索引。

        Returns:
            int: 文本文件中作为值的列索引。
        """
        return self.value_index 