import pandas as pd
from typing import Any

from intefaces.output_strategy import LoadStrategy
from intefaces.source import Source

class DataFrameSource(Source):
    def __init__(self, data: pd.DataFrame = None):
        self.data = data if data is not None else pd.DataFrame()

    def load(self, strategy: 'LoadStrategy', source: str) -> None:
        """使用加载策略从指定源加载数据为DataFrame"""
        loaded_data = strategy.load_from(source)
        self.deserialize(loaded_data)

    def serialize(self) -> dict:
        """将DataFrame序列化为字典"""
        return self.data.to_dict(orient='records')

    def deserialize(self, data: dict) -> None:
        """从字典反序列化为DataFrame"""
        self.data = pd.DataFrame(data)

    @classmethod
    def from_data(cls, data: pd.DataFrame):
        """替代构造器的反序列化方法"""
        return cls(data.copy())