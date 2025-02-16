import yaml
from typing import Dict, Any
from workflow.interfaces.loader_interface import LoaderInterface
from workflow.core.task import task
from workflow.core.step import Step
from workflow.core.source import Source
from workflow.core.destination import Destination

class YamlTaskLoader(LoaderInterface):
    """
    YAML 任务加载器。
    
    用于从 YAML 文件加载任务。
    """

    def __init__(self):
        self.type = 'yaml_task'
        self.options = {}

    def load(self, path: str) -> Dict[str, Any]:
        """
        加载指定路径的 YAML 文件并解析为任务。

        Args:
            path (str): YAML 文件路径。

        Returns:
            Dict[str, Any]: 解析后的任务配置。
        """
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def create_task(self, task_config: Dict[str, Any]):
        """
        根据任务配置创建任务。

        Args:
            task_config (Dict[str, Any]): 任务配置。

        Returns:
            Task: 创建的任务对象。
        """
        @task
        def task_func():
            for step_config in task_config.get('steps', []):
                step = self.create_step(step_config)
                step.execute()

        return task_func

    def create_step(self, step_config: Dict[str, Any]) -> Step:
        """
        根据步骤配置创建步骤。

        Args:
            step_config (Dict[str, Any]): 步骤配置。

        Returns:
            Step: 创建的步骤对象。
        """
        step = Step(name=step_config.get('name', 'Step'))
        if 'sources' in step_config:
            step.set_sources([Source(path, 'file') for path in step_config['sources']])
        if 'destination' in step_config:
            step.set_destination(Destination(step_config['destination'], 'file'))
        return step

    def is_supported(self, path: str) -> bool:
        """
        判断是否支持加载指定路径的 YAML 文件。

        Args:
            path (str): 文件路径。

        Returns:
            bool: 如果支持，返回 True；否则返回 False。
        """
        return path.endswith('.yaml') or path.endswith('.yml')

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。

        Args:
            data (Any): 加载后的数据。

        Returns:
            Any: 转换后的数据。
        """
        return data 