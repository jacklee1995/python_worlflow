from abc import ABC, abstractmethod
from typing import Any

from intefaces.load_stategy import LoadStrategy
from intefaces.output_strategy import OutputStrategy


class Source(ABC):
    """
    资源接口。

    资源表示可以被任务利用的数据或对象。资源通过加载器（Loader）使用特定的加载策略进行加载。

    Attributes:
        无

    Methods:
        load(strategy: LoadStrategy, source: str) -> None:
            使用指定的加载策略从源加载资源。

        output(strategy: OutputStrategy, target: str) -> None:
            使用指定的输出策略将资源输出到目标。

        get_data() -> Any:
            获取资源的数据。

        set_data(data: Any) -> None:
            设置资源的数据。

        append_data(data: Any) -> None:
            追加数据到资源。

        clear_data() -> None:
            清空资源的数据。

        serialize() -> Any:
            将资源序列化为可存储的格式。

        deserialize(data: Any) -> None:
            从序列化的数据中反序列化资源。
    """

    @abstractmethod
    def load(self, strategy: LoadStrategy, source: str) -> None:
        """
        使用指定的加载策略从源加载资源。

        Args:
            strategy (LoadStrategy): 加载策略。
            source (str): 资源的源。

        Returns:
            None
        """
        pass

    @abstractmethod
    def output(self, strategy: OutputStrategy, target: str) -> None:
        """
        使用指定的输出策略将资源输出到目标。

        Args:
            strategy (OutputStrategy): 输出策略。
            target (str): 输出的目标。

        Returns:
            None
        """
        pass

    @abstractmethod
    def get_data(self) -> Any:
        """
        获取资源的数据。

        Returns:
            Any: 资源的数据。
        """
        pass

    @abstractmethod
    def set_data(self, data: Any) -> None:
        """
        设置资源的数据。

        Args:
            data (Any): 要设置的数据。

        Returns:
            None
        """
        pass

    @abstractmethod
    def append_data(self, data: Any) -> None:
        """
        追加数据到资源。

        Args:
            data (Any): 要追加的数据。

        Returns:
            None
        """
        pass

    @abstractmethod
    def clear_data(self) -> None:
        """
        清空资源的数据。

        Returns:
            None
        """
        pass

    @abstractmethod
    def serialize(self) -> Any:
        """
        将资源序列化为可存储的格式。

        Returns:
            Any: 序列化后的资源数据。
        """
        pass

    @abstractmethod
    def deserialize(self, data: Any) -> None:
        """
        从序列化的数据中反序列化资源。

        Args:
            data (Any): 序列化的资源数据。

        Returns:
            None
        """
        pass