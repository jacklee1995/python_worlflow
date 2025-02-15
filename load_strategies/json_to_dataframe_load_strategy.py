import pandas as pd

from intefaces.load_stategy import LoadStrategy
from sources.dataframe_source import DataFrameSource


class JsonToDataFrameLoadStrategy(LoadStrategy):
    """
    JSON 转 DataFrame 加载策略。

    该策略用于将 JSON 文件加载为 DataFrameSource。

    Attributes:
        orient (str): JSON 字符串的数据方向，默认为 'records'。

    Methods:
        load() -> DataFrameSource:
            从指定源加载 JSON 数据，并转换为 DataFrameSource。

        set_orient(orient: str) -> None:
            设置 JSON 字符串的数据方向。

        get_orient() -> str:
            获取 JSON 字符串的数据方向。
    """

    def __init__(self, source: str, orient: str = 'records'):
        """
        初始化 JsonToDataFrameLoadStrategy 实例。

        Args:
            source (str): JSON 文件的路径。
            orient (str, optional): JSON 字符串的数据方向，默认为 'records'。
        """
        super().__init__(source)
        self.orient = orient

    def load(self) -> DataFrameSource:
        """
        从指定源加载 JSON 数据，并转换为 DataFrameSource。

        Returns:
            DataFrameSource: 加载并转换后的 DataFrameSource 对象。
        """
        df = pd.read_json(self.source, orient=self.orient)
        return DataFrameSource(df)

    def set_orient(self, orient: str) -> None:
        """
        设置 JSON 字符串的数据方向。

        Args:
            orient (str): JSON 字符串的数据方向。

        Returns:
            None
        """
        self.orient = orient

    def get_orient(self) -> str:
        """
        获取 JSON 字符串的数据方向。

        Returns:
            str: JSON 字符串的数据方向。
        """
        return self.orient 