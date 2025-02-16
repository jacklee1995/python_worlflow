import argparse
import os
from typing import Optional

from workflow.core.destination import Destination
from workflow.core.source import Source
from workflow.core.workflow import Workflow
from workflow.core.config import Config
from workflow.steps.split_step import SplitStep

def split_command(task_name: Optional[str] = None, mode: str = "development"):
    """
    运行数据分割任务。

    Args:
        task_name (Optional[str]): 任务名称。如果未提供，则运行默认任务。
        mode (str): 运行模式，如 "development" 或 "production"。
    """
    # 加载环境变量
    load_env_vars(mode)

    # 加载配置
    config = Config()
    config.load()

    # 创建 Workflow 实例
    workflow = Workflow()

    # 创建 SplitStep 实例
    split_step = SplitStep()

    # 设置数据源和输出目标
    split_step.set_sources([Source("data/input.csv")])
    split_step.set_destination(Destination("data/output.csv"))

    # 设置分割参数
    split_step.set_split_by(["category"])

    # 添加步骤到任务
    workflow.add_step(split_step)

    # 运行任务
    if task_name:
        workflow.run_task(task_name)
    else:
        workflow.run_default_task()

def load_env_vars(mode: str):
    """
    加载环境变量。

    Args:
        mode (str): 运行模式，如 "development" 或 "production"。
    """
    # 加载 .env 文件
    from dotenv import load_dotenv
    load_dotenv()

    # 加载特定模式的环境变量文件
    env_files = [".env", f".env.{mode}", f".env.{mode}.local"]
    for env_file in env_files:
        if os.path.exists(env_file):
            load_dotenv(env_file)