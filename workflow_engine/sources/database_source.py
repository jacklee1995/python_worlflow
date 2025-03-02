import asyncio
from typing import Optional, AsyncIterator, List, Dict, Any
import aiomysql

from workflow_engine.core.source import Source
from workflow_engine.interfaces.source_interface import StreamMode


class DatabaseSource(Source):
    """数据库数据源,支持从 MySQL 数据库读取数据"""

    def __init__(self, host: str, port: int, user: str, password: str, db: str, 
                 query: str, mode: StreamMode = 'r'):
        super().__init__(f"mysql://{host}:{port}/{db}", mode)
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._db = db
        self._query = query
        self._pool: Optional[aiomysql.Pool] = None
        self._conn: Optional[aiomysql.Connection] = None
        self._cursor: Optional[aiomysql.Cursor] = None

    async def open(self, mode: StreamMode = 'r') -> None:
        """打开数据库连接"""
        if 'r' not in mode:
            raise ValueError(f"Unsupported mode: {mode}")
        self._pool = await aiomysql.create_pool(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._password,
            db=self._db,
            autocommit=True
        )
        self._conn = await self._pool.acquire()
        self._cursor = await self._conn.cursor()

    async def close(self) -> None:
        """关闭数据库连接"""
        if self._cursor:
            await self._cursor.close()
            self._cursor = None
        if self._conn:
            self._pool.release(self._conn)
            self._conn = None
        if self._pool:
            self._pool.close()
            await self._pool.wait_closed()
            self._pool = None

    async def read(self, n: int = -1) -> List[Dict[str, Any]]:
        """读取数据库数据"""
        if not self._cursor:
            raise RuntimeError("Database connection not opened")
        await self._cursor.execute(self._query)
        if n == -1:
            return await self._cursor.fetchall()
        else:
            return await self._cursor.fetchmany(n)

    async def readlines(self) -> AsyncIterator[Dict[str, Any]]:
        """逐行读取数据库数据"""
        if not self._cursor:
            raise RuntimeError("Database connection not opened")
        await self._cursor.execute(self._query)
        async for row in self._cursor:
            yield row

    async def write(self, data: Dict[str, Any]) -> None:
        """写入数据库数据(不支持)"""
        raise NotImplementedError("DatabaseSource does not support write operation")

    async def writelines(self, lines: AsyncIterator[Dict[str, Any]]) -> None:
        """逐行写入数据库数据(不支持)"""
        raise NotImplementedError("DatabaseSource does not support write operation")

    def get_size(self) -> Optional[int]:
        """获取数据大小(不支持)"""
        return None

    def is_seekable(self) -> bool:
        """判断是否可随机访问"""
        return False

    def seek(self, offset: int, whence: int = 0) -> None:
        """移动读写指针(不支持)"""
        raise NotImplementedError("DatabaseSource does not support seek operation")

    def tell(self) -> int:
        """获取当前读写指针位置(不支持)"""
        raise NotImplementedError("DatabaseSource does not support tell operation") 