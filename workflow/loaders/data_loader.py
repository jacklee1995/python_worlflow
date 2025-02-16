import pandas as pd
from typing import Any, Dict, List
from workflow.interfaces.loader_interface import LoaderInterface
from workflow.core.source import Source

class DataLoader(LoaderInterface):
    """
    数据加载器。
    
    用于加载数据文件（如 Parquet、Feather 等），并将其解析为 Pandas DataFrame 或其他数据结构。
    """

    def __init__(self):
        self.type = 'data'
        self.options = {}

    def load(self, path: str) -> Any:
        """
        加载指定路径的数据文件并解析为 Pandas DataFrame 或其他数据结构。

        Args:
            path (str): 数据文件路径。

        Returns:
            Any: 解析后的数据对象。
        """
        if path.endswith('.parquet'):
            return pd.read_parquet(path)
        elif path.endswith('.feather'):
            return pd.read_feather(path)
        elif path.endswith('.csv'):
            return pd.read_csv(path)
        elif path.endswith('.json'):
            return pd.read_json(path)
        else:
            raise ValueError(f"Unsupported data format: {path}")

    def is_supported(self, path: str) -> bool:
        """
        判断是否支持加载指定路径的数据文件。

        Args:
            path (str): 文件路径。

        Returns:
            bool: 如果支持，返回 True；否则返回 False。
        """
        return path.endswith(('.parquet', '.feather', '.csv', '.json'))

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。

        Args:
            data (Any): 加载后的数据。

        Returns:
            Any: 转换后的数据。
        """
        return data
