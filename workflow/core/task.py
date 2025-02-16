from typing import Callable, List, Dict, Optional
from workflow.interfaces.task_interface import TaskInterface
from workflow.interfaces.step_interface import StepInterface
from workflow.interfaces.config_interface import ConfigInterface
import os

def task(func: Callable) -> TaskInterface:
    """
    任务装饰器，将函数转换为任务。

    Args:
        func (Callable): 要转换为任务的函数。

    Returns:
        TaskInterface: 任务对象。
    """
    class Task(TaskInterface):
        def __init__(self, func: Callable):
            self.func = func
            self.steps: List[StepInterface] = []
            self.config: Optional[ConfigInterface] = None
            self.env_vars: Dict[str, str] = {}

        def execute(self) -> None:
            """
            执行任务，包括加载配置和环境变量，并依次执行所有步骤。
            """
            # 加载环境变量
            self._load_env_vars()

            # 执行任务函数
            self.func()

            # 执行所有步骤
            for step in self.steps:
                if self.config:
                    step.set_config(self.config)
                step.execute()

        def _load_env_vars(self) -> None:
            """
            加载环境变量。
            """
            self.env_vars = dict(os.environ)

        def add_step(self, step: StepInterface) -> None:
            """
            添加步骤到任务中。

            Args:
                step (StepInterface): 要添加的步骤。
            """
            self.steps.append(step)

        def get_steps(self) -> List[StepInterface]:
            """
            获取任务的所有步骤。

            Returns:
                List[StepInterface]: 任务的所有步骤。
            """
            return self.steps

        def set_config(self, config: ConfigInterface) -> None:
            """
            设置任务的配置。

            Args:
                config (ConfigInterface): 任务的配置。
            """
            self.config = config

        def get_config(self) -> Optional[ConfigInterface]:
            """
            获取任务的配置。

            Returns:
                Optional[ConfigInterface]: 任务的配置。
            """
            return self.config

        def get_env_var(self, key: str, default: Optional[str] = None) -> Optional[str]:
            """
            获取环境变量的值。

            Args:
                key (str): 环境变量的键。
                default (Optional[str]): 默认值，当键不存在时返回。

            Returns:
                Optional[str]: 环境变量的值，如果键不存在，则返回默认值。
            """
            return self.env_vars.get(key, default)

    return Task(func)
