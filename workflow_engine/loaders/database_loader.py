import sqlite3
from typing import Any, Dict, List
from workflow_engine.interfaces.loader_interface import LoaderInterface
from workflow_engine.core.source import Source

class DatabaseLoader(LoaderInterface):
    """
    数据库加载器。
    
    用于加载数据库文件（如 SQLite、SQL 脚本等），并将其解析为数据库连接或查询结果。
    """

    def __init__(self):
        self.type = 'database'
        self.options = {}

    def load(self, path: str) -> Any:
        """
        加载指定路径的数据库文件并返回数据库连接或查询结果。

        Args:
            path (str): 数据库文件路径。

        Returns:
            Any: 数据库连接或查询结果。
        """
        if not path.endswith(('.db', '.sqlite', '.sqlite3')):
            raise ValueError(f"Unsupported database format: {path}")

        conn = sqlite3.connect(path)
        return conn

    def execute_query(self, conn: Any, query: str) -> List[Dict[str, Any]]:
        """
        执行 SQL 查询并返回结果。

        Args:
            conn (Any): 数据库连接对象。
            query (str): SQL 查询语句。

        Returns:
            List[Dict[str, Any]]: 查询结果列表。
        """
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    def is_supported(self, path: str) -> bool:
        """
        判断是否支持加载指定路径的数据库文件。

        Args:
            path (str): 文件路径。

        Returns:
            bool: 如果支持，返回 True；否则返回 False。
        """
        return path.endswith(('.db', '.sqlite', '.sqlite3'))

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。

        Args:
            data (Any): 加载后的数据。

        Returns:
            Any: 转换后的数据。
        """
        return data
