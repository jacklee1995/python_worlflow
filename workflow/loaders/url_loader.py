from typing import Any, List
import requests

from workflow.interfaces.loader_interface import LoaderInterface
from workflow.interfaces.source_interface import SourceInterface
from workflow.core.source import Source


class UrlLoader(LoaderInterface):
    """
    URL 加载器。

    用于加载指定 URL 的资源。
    """

    def __init__(self, allowed_schemes: List[str] = None):
        """
        初始化 UrlLoader。

        Args:
            allowed_schemes (List[str]): 允许加载的 URL 协议列表。默认为 None，表示允许所有协议。
        """
        self.allowed_schemes = allowed_schemes or []
        self.type = 'url'
        self.options = {}

    def load(self, url: str) -> SourceInterface:
        """
        加载指定 URL 的资源。

        Args:
            url (str): 资源的 URL。

        Returns:
            SourceInterface: 加载后的资源对象。

        Raises:
            ValueError: 如果 URL 的协议不在允许的协议列表中。
            requests.exceptions.RequestException: 如果加载 URL 资源失败。
        """
        if not self.is_supported(url):
            raise ValueError(f"Unsupported URL scheme for {url}.")

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.text
            source = Source(url, 'url', data)
            return source
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Failed to load URL {url}. Error: {str(e)}")

    def get_extensions(self) -> List[str]:
        """
        获取允许加载的文件扩展名列表。

        对于 URL 加载器，返回空列表，因为 URL 没有文件扩展名的概念。

        Returns:
            List[str]: 允许加载的文件扩展名列表。
        """
        return []

    def set_extensions(self, extensions: List[str]) -> None:
        """
        设置允许加载的文件扩展名列表。

        对于 URL 加载器，该方法不执行任何操作，因为 URL 没有文件扩展名的概念。

        Args:
            extensions (List[str]): 允许加载的文件扩展名列表。
        """
        pass

    def get_type(self) -> str:
        """
        获取加载器的类型。

        Returns:
            str: 加载器的类型。
        """
        return self.type

    def set_type(self, loader_type: str) -> None:
        """
        设置加载器的类型。

        Args:
            loader_type (str): 加载器的类型。
        """
        self.type = loader_type

    def get_options(self) -> dict:
        """
        获取加载器的选项。

        Returns:
            dict: 加载器的选项。
        """
        return self.options

    def set_options(self, options: dict) -> None:
        """
        设置加载器的选项。

        Args:
            options (dict): 加载器的选项。
        """
        self.options = options

    def is_supported(self, url: str) -> bool:
        """
        判断是否支持加载指定 URL 的资源。

        Args:
            url (str): 资源的 URL。

        Returns:
            bool: 如果支持，返回 True；否则返回 False。
        """
        scheme = url.split('://')[0]
        return scheme in self.allowed_schemes or not self.allowed_schemes

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。

        Args:
            data (Any): 加载后的数据。

        Returns:
            Any: 转换后的数据。
        """
        return data