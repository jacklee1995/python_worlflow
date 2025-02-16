import configparser
from typing import Any, Dict
from workflow.interfaces.loader_interface import LoaderInterface
from workflow.core.source import Source

class ConfigLoader(LoaderInterface):
    """
    配置文件加载器。
    
    用于加载 .config 或 .conf 配置文件，并将其解析为 Python 字典。
    """

    def __init__(self):
        self.type = 'config'
        self.options = {}

    def load(self, path: str) -> Dict[str, Any]:
        """
        加载指定路径的配置文件并解析为 Python 字典。

        Args:
            path (str): 配置文件路径。

        Returns:
            Dict[str, Any]: 解析后的 Python 字典。
        """
        config = configparser.ConfigParser()
        config.read(path)
        return {section: dict(config[section]) for section in config.sections()}

    def is_supported(self, path: str) -> bool:
        """
        判断是否支持加载指定路径的配置文件。

        Args:
            path (str): 文件路径。

        Returns:
            bool: 如果支持，返回 True；否则返回 False。
        """
        return path.endswith(('.config', '.conf'))

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。

        Args:
            data (Any): 加载后的数据。

        Returns:
            Any: 转换后的数据。
        """
        return data
