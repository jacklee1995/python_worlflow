import yaml
from typing import Any

from intefaces.load_stategy import LoadStrategy
from intefaces.output_strategy import OutputStrategy
from intefaces.source import Source


class YamlSource(Source):
    """
    YAML 资源类。

    该类表示以 YAML 格式存储的数据资源，内部使用字典存储数据。

    Attributes:
        data (dict): YAML 数据，使用字典存储。

    Methods:
        load(strategy: LoadStrategy, source: str) -> None:
            使用指定的加载策略从源加载 YAML 数据。

        output(strategy: OutputStrategy, target: str) -> None:
            使用指定的输出策略将 YAML 数据输出到目标。

        get_data() -> dict:
            获取 YAML 数据的字典。

        set_data(data: dict) -> None:
            设置 YAML 数据的字典。

        update_data(data: dict) -> None:
            使用新的字典更新 YAML 数据。

        clear_data() -> None:
            清空 YAML 数据的字典。

        serialize() -> str:
            将 YAML 数据序列化为字符串。

        deserialize(data: str) -> None:
            从字符串反序列化 YAML 数据。

        from_data(data: dict) -> 'YamlSource':
            从字典创建 YamlSource 实例的替代构造器。
    """

    def __init__(self, data: dict = None):
        """
        初始化 YamlSource 实例。

        Args:
            data (dict, optional): YAML 数据的字典。默认为 None，表示创建空的字典。
        """
        self.data = data if data is not None else {}

    def load(self, strategy: LoadStrategy, source: str) -> None:
        """
        使用指定的加载策略从源加载 YAML 数据。

        Args:
            strategy (LoadStrategy): 加载策略。
            source (str): YAML 数据的源。

        Returns:
            None
        """
        loaded_data = strategy.load_from(source)
        self.deserialize(loaded_data)

    def output(self, strategy: OutputStrategy, target: str) -> None:
        """
        使用指定的输出策略将 YAML 数据输出到目标。

        Args:
            strategy (OutputStrategy): 输出策略。
            target (str): 输出的目标。

        Returns:
            None
        """
        serialized_data = self.serialize()
        strategy.output_to(target, serialized_data)

    def get_data(self) -> dict:
        """
        获取 YAML 数据的字典。

        Returns:
            dict: YAML 数据的字典。
        """
        return self.data.copy()

    def set_data(self, data: dict) -> None:
        """
        设置 YAML 数据的字典。

        Args:
            data (dict): 要设置的字典数据。

        Returns:
            None
        """
        self.data = data.copy()

    def update_data(self, data: dict) -> None:
        """
        使用新的字典更新 YAML 数据。

        Args:
            data (dict): 要更新的字典数据。

        Returns:
            None
        """
        self.data.update(data)

    def clear_data(self) -> None:
        """
        清空 YAML 数据的字典。

        Returns:
            None
        """
        self.data.clear()

    def serialize(self) -> str:
        """
        将 YAML 数据序列化为字符串。

        Returns:
            str: 序列化后的 YAML 字符串。
        """
        return yaml.dump(self.data)

    def deserialize(self, data: str) -> None:
        """
        从字符串反序列化 YAML 数据。

        Args:
            data (str): 序列化的 YAML 字符串。

        Returns:
            None
        """
        self.data = yaml.safe_load(data)

    @classmethod
    def from_data(cls, data: dict) -> 'YamlSource':
        """
        从字典创建 YamlSource 实例的替代构造器。

        Args:
            data (dict): YAML 数据的字典。

        Returns:
            YamlSource: 创建的 YamlSource 实例。
        """
        return cls(data.copy()) 