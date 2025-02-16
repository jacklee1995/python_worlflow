import yaml
import json

from intefaces.load_stategy import LoadStrategy
from sources.json_source import JsonSource


class YamlToJsonLoadStrategy(LoadStrategy):
    """
    YAML 转 JSON 加载策略。

    该策略用于将 YAML 文件加载为 JsonSource。

    Attributes:
        无

    Methods:
        load() -> JsonSource:
            从指定源加载 YAML 数据，并转换为 JsonSource。
    """

    def load(self) -> JsonSource:
        """
        从指定源加载 YAML 数据，并转换为 JsonSource。

        Returns:
            JsonSource: 加载并转换后的 JsonSource 对象。
        """
        with open(self.source, 'r') as file:
            yaml_data = yaml.safe_load(file)
            json_data = json.dumps(yaml_data)
            return JsonSource.from_data(json.loads(json_data)) 