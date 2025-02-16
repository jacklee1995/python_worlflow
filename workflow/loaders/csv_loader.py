import csv
from typing import Any, List, Dict
from workflow.interfaces.loader_interface import LoaderInterface
from workflow.core.source import Source

class CsvLoader(LoaderInterface):
    """
    CSV 加载器。
    
    用于加载 CSV 文件，并将其解析为 Python 列表或字典。
    """

    def __init__(self):
        self.type = 'csv'
        self.options = {}

    def load(self, path: str) -> List[Dict[str, Any]]:
        """
        加载指定路径的 CSV 文件并解析为 Python 列表或字典。

        Args:
            path (str): CSV 文件路径。

        Returns:
            List[Dict[str, Any]]: 解析后的 Python 列表或字典。
        """
        with open(path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [row for row in reader]

    def is_supported(self, path: str) -> bool:
        """
        判断是否支持加载指定路径的 CSV 文件。

        Args:
            path (str): 文件路径。

        Returns:
            bool: 如果支持，返回 True；否则返回 False。
        """
        return path.endswith('.csv')

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。

        Args:
            data (Any): 加载后的数据。

        Returns:
            Any: 转换后的数据。
        """
        return data
