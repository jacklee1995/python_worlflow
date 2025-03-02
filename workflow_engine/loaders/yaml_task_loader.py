import os
import yaml
from typing import Dict, Any
from workflow_engine.interfaces.loader_interface import LoaderInterface
from workflow_engine.core.task import task
from workflow_engine.core.step import Step
from workflow_engine.core.source import Source
from workflow_engine.core.output import Output
from workflow_engine.interfaces.output_strategy import OutputStrategy
from workflow_engine.logging import logger

class YamlTaskLoader(LoaderInterface):
    """
    YAML任务加载器。
    
    用于从YAML文件加载任务。
    """

    def __init__(self):
        self.type = 'yaml_task'
        self.options = {}

    def load(self, path: str) -> Dict[str, Any]:
        """
        加载指定路径的YAML文件并解析为任务。

        Args:
            path (str): YAML文件路径。

        Returns:
            Dict[str, Any]: 解析后的任务配置。
        """
        if not self.is_supported(path):
            raise ValueError(f"Unsupported file type: {path}")
        
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"File not found: {path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML format in {path}: {str(e)}")
            raise

    def create_task(self, task_config: Dict[str, Any]):
        """
        根据任务配置创建任务。

        Args:
            task_config (Dict[str, Any]): 任务配置。

        Returns:
            Task: 创建的任务对象。
        """
        @task(name=task_config.get('name', 'Task'), 
              description=task_config.get('description', 'A task loaded from YAML'))
        async def task_func():
            config = task_config.get('config', {})
            # TODO: 处理任务级别的配置
            
            for step_config in task_config.get('steps', []):
                step = await self.create_step(step_config)
                await step.execute()

        return task_func

    async def create_step(self, step_config: Dict[str, Any]) -> Step:
        """
        根据步骤配置创建步骤。

        Args:
            step_config (Dict[str, Any]): 步骤配置。

        Returns:
            Step: 创建的步骤对象。
        """
        step = Step(name=step_config.get('name', 'Step'),
                    description=step_config.get('description', 'A step in task'))
        
        if 'config' in step_config:
            step.set_config(step_config['config'])
        
        if 'sources' in step_config:
            sources = [Source(uri=uri) for uri in step_config['sources']]
            step.set_sources(sources)
        
        if 'output' in step_config:
            output_config = step_config['output']
            strategy_class = output_config.pop('type', 'console')
            strategy = self.create_output_strategy(strategy_class, output_config)
            output = Output(strategy=strategy)
            step.set_output(output)
        
        return step

    def create_output_strategy(self, strategy_type: str, config: Dict[str, Any]) -> OutputStrategy:
        """
        根据输出策略类型和配置创建输出策略。

        Args:
            strategy_type (str): 输出策略类型。
            config (Dict[str, Any]): 输出策略配置。

        Returns:
            OutputStrategy: 创建的输出策略对象。
        """
        strategy_map = {
            'console': 'ConsoleOutputStrategy',
            'file': 'FileOutputStrategy',
            'network': 'NetworkOutputStrategy',
            'email': 'EmailOutputStrategy'
        }
        
        class_name = strategy_map.get(strategy_type)
        if not class_name:
            raise ValueError(f"Unsupported output strategy type: {strategy_type}")
        
        try:
            module = __import__('workflow.core.output_strategies', fromlist=[class_name])
            strategy_class = getattr(module, class_name)
            return strategy_class(**config)
        except (ImportError, AttributeError):
            logger.error(f"Failed to load output strategy: {class_name}")
            raise
        except TypeError as e:
            logger.error(f"Invalid configuration for {class_name}: {str(e)}")
            raise

    def is_supported(self, path: str) -> bool:
        """
        判断是否支持加载指定路径的YAML文件。

        Args:
            path (str): 文件路径。

        Returns:
            bool: 如果支持,返回True；否则返回False。
        """
        if not os.path.isfile(path):
            return False
        
        _, ext = os.path.splitext(path)
        return ext in ('.yaml', '.yml')

    def transform(self, data: Any) -> Any:
        """
        对加载后的数据进行转换。

        Args:
            data (Any): 加载后的数据。

        Returns:
            Any: 转换后的数据。
        """
        return data
    
    def __repr__(self):
        return f"YamlTaskLoader(type={self.type}, options={self.options})"
    
    def __str__(self):
        return self.__repr__() 