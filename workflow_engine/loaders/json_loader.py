import json
from typing import Any, Dict
from workflow_engine.interfaces.loader_interface import LoaderInterface
from workflow_engine.core.source import Source

class JsonLoader(LoaderInterface):
    """
    JSON 加载器。
    
    用于加载 JSON 文件，并将其解析为 Python 字典或列表。
    """

    def __init__(self):
        self.type = 'json'
        self.options = {}

    def load(self, path: str) -> Dict[str, Any]:
        """
        加载指定路径的 JSON 文件并解析为 Python 字典或列表。

        Args:
            path (str): JSON 文件路径。

        Returns:
            Dict[str, Any]: 解析后的 Python 字典或列表。
        """
        with open(path, 'r') as f:
            return json.load(f)

    def is_supported(self, path: str) -> bool:
        """
        判断是否支持加载指定路径的 JSON 文件。

        Args:
            path (str): 文件路径。

        Returns:
            bool: 如果支持，返回 True；否则返回 False。
        """
        return path.endswith('.json')

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。

        Args:
            data (Any): 加载后的数据。

        Returns:
            Any: 转换后的数据。
        """
        return data
