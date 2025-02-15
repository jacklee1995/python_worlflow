import asyncio

from intefaces.load_stategy import LoadStrategy


class TextToStringLoadStrategy(LoadStrategy):
    """
    文本转字符串加载策略。

    该策略用于将文本文件异步加载为字符串。

    Attributes:
        trim (bool): 是否去除字符串首尾空白字符，默认为 True。

    Methods:
        load() -> str:
            从指定源异步加载文本数据，并转换为字符串。

        set_trim(trim: bool) -> None:
            设置是否去除字符串首尾空白字符。

        get_trim() -> bool:
            获取是否去除字符串首尾空白字符。
    """

    def __init__(self, source: str, trim: bool = True):
        """
        初始化 TextToStringLoadStrategy 实例。

        Args:
            source (str): 文本文件的路径。
            trim (bool, optional): 是否去除字符串首尾空白字符，默认为 True。
        """
        super().__init__(source)
        self.trim = trim

    async def load(self) -> str:
        """
        从指定源异步加载文本数据，并转换为字符串。

        Returns:
            str: 加载并转换后的字符串。
        """
        async with asyncio.open(self.source, mode='r') as file:
            content = await file.read()
            if self.trim:
                content = content.strip()
            return content

    def set_trim(self, trim: bool) -> None:
        """
        设置是否去除字符串首尾空白字符。

        Args:
            trim (bool): 是否去除字符串首尾空白字符。

        Returns:
            None
        """
        self.trim = trim

    def get_trim(self) -> bool:
        """
        获取是否去除字符串首尾空白字符。

        Returns:
            bool: 是否去除字符串首尾空白字符。
        """
        return self.trim
