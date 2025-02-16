import pandas as pd
from typing import Any

from ..intefaces.load_stategy import LoadStrategy
from ..intefaces.source import Source

class XlsxSource(Source):
    def __init__(self, data: pd.DataFrame = None):
        self.data = data if data is not None else pd.DataFrame()

    def load(self, strategy: 'LoadStrategy', source: str) -> None:
        """使用加载策略从指定源加载XLSX数据"""
        loaded_data = strategy.load_from(source)
        self.deserialize(loaded_data)

    def serialize(self) -> bytes:
        """将DataFrame序列化为XLSX二进制数据"""
        with pd.ExcelWriter("temp.xlsx", engine="openpyxl") as writer:
            self.data.to_excel(writer, index=False)
        with open("temp.xlsx", "rb") as f:
            return f.read()

    def deserialize(self, data: bytes) -> None:
        """从XLSX二进制数据反序列化为DataFrame"""
        with open("temp.xlsx", "wb") as f:
            f.write(data)
        self.data = pd.read_excel("temp.xlsx")

    @classmethod
    def from_data(cls, data: pd.DataFrame):
        """替代构造器的反序列化方法"""
        return cls(data.copy())