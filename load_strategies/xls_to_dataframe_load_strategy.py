import pandas as pd

from intefaces.load_stategy import LoadStrategy
from sources.dataframe_source import DataFrameSource


class XLSToDataFrameLoadStrategy(LoadStrategy):
    """
    XLS 转 DataFrame 加载策略。

    该策略用于将 XLS 文件加载为 DataFrameSource。

    Attributes:
        sheet_name (str): 要加载的工作表名称，默认为 0，表示第一个工作表。
        header (int): XLS 文件的表头行索引，默认为 0，表示第一行为表头。

    Methods:
        load() -> DataFrameSource:
            从指定源加载 XLS 数据，并转换为 DataFrameSource。

        set_sheet_name(sheet_name: str) -> None:
            设置要加载的工作表名称。

        get_sheet_name() -> str:
            获取要加载的工作表名称。

        set_header(header: int) -> None:
            设置 XLS 文件的表头行索引。

        get_header() -> int:
            获取 XLS 文件的表头行索引。
    """

    def __init__(self, source: str, sheet_name: str = 0, header: int = 0):
        """
        初始化 XLSToDataFrameLoadStrategy 实例。

        Args:
            source (str): XLS 文件的路径。
            sheet_name (str, optional): 要加载的工作表名称，默认为 0，表示第一个工作表。
            header (int, optional): XLS 文件的表头行索引，默认为 0，表示第一行为表头。
        """
        super().__init__(source)
        self.sheet_name = sheet_name
        self.header = header

    def load(self) -> DataFrameSource:
        """
        从指定源加载 XLS 数据，并转换为 DataFrameSource。

        Returns:
            DataFrameSource: 加载并转换后的 DataFrameSource 对象。
        """
        df = pd.read_excel(self.source, sheet_name=self.sheet_name, header=self.header)
        return DataFrameSource(df)

    def set_sheet_name(self, sheet_name: str) -> None:
        """
        设置要加载的工作表名称。

        Args:
            sheet_name (str): 要加载的工作表名称。

        Returns:
            None
        """
        self.sheet_name = sheet_name

    def get_sheet_name(self) -> str:
        """
        获取要加载的工作表名称。

        Returns:
            str: 要加载的工作表名称。
        """
        return self.sheet_name

    def set_header(self, header: int) -> None:
        """
        设置 XLS 文件的表头行索引。

        Args:
            header (int): XLS 文件的表头行索引。

        Returns:
            None
        """
        self.header = header

    def get_header(self) -> int:
        """
        获取 XLS 文件的表头行索引。

        Returns:
            int: XLS 文件的表头行索引。
        """
        return self.header 