import os
from typing import Dict, Any
from workflow.interfaces.loader_interface import LoaderInterface
from workflow.core.source import Source

class EnvLoader(LoaderInterface):
    """
    环境变量加载器。
    
    用于加载环境变量文件（如 .env），并将其解析为 Python 字典。
    """

    def __init__(self):
        self.type = 'env'
        self.options = {}

    def load(self, path: str) -> Dict[str, Any]:
        """
        加载指定路径的环境变量文件并解析为 Python 字典。

        Args:
            path (str): 环境变量文件路径。

        Returns:
            Dict[str, Any]: 解析后的环境变量字典。
        """
        env_vars = {}
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
        return env_vars

    def is_supported(self, path: str) -> bool:
        """
        判断是否支持加载指定路径的环境变量文件。

        Args:
            path (str): 文件路径。

        Returns:
            bool: 如果支持，返回 True；否则返回 False。
        """
        return path.endswith('.env')

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。

        Args:
            data (Any): 加载后的数据。

        Returns:
            Any: 转换后的数据。
        """
        return data
