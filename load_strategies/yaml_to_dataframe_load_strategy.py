import yaml
import pandas as pd

from intefaces.load_stategy import LoadStrategy
from sources.dataframe_source import DataFrameSource


class YamlToDataFrameLoadStrategy(LoadStrategy):
    """
    YAML 转 DataFrame 加载策略。

    该策略用于将 YAML 文件加载为 DataFrameSource。

    Attributes:
        无

    Methods:
        load() -> DataFrameSource:
            从指定源加载 YAML 数据，并转换为 DataFrameSource。
    """

    def load(self) -> DataFrameSource:
        """
        从指定源加载 YAML 数据，并转换为 DataFrameSource。

        Returns:
            DataFrameSource: 加载并转换后的 DataFrameSource 对象。
        """
        with open(self.source, 'r') as file:
            yaml_data = yaml.safe_load(file)
            df = pd.DataFrame(yaml_data)
            return DataFrameSource(df) 