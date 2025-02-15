import json
import yaml

from intefaces.load_stategy import LoadStrategy
from sources.yaml_source import YamlSource


class JsonToYamlLoadStrategy(LoadStrategy):
    """
    JSON 转 YAML 加载策略。

    该策略用于将 JSON 文件加载为 YamlSource。

    Attributes:
        无

    Methods:
        load() -> YamlSource:
            从指定源加载 JSON 数据，并转换为 YamlSource。
    """

    def load(self) -> YamlSource:
        """
        从指定源加载 JSON 数据，并转换为 YamlSource。

        Returns:
            YamlSource: 加载并转换后的 YamlSource 对象。
        """
        with open(self.source, 'r') as file:
            json_data = json.load(file)
            yaml_data = yaml.dump(json_data)
            return YamlSource.from_data(yaml.safe_load(yaml_data)) 