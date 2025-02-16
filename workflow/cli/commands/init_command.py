import os
import shutil
from pathlib import Path
from typing import Optional

from workflow.cli.templates import get_template_path
from workflow.cli.commands.utils import prompt_user, create_project_structure

def init_command(project_name: Optional[str] = None, template: str = "project"):
    """
    初始化一个新的 Workflow 项目。

    Args:
        project_name (Optional[str]): 项目名称。如果未提供，则提示用户输入。
        template (str): 使用的模板类型，可以是 "project" 或 "single_file"。
    """
    if not project_name:
        project_name = prompt_user("请输入项目名称: ")

    # 获取模板路径
    template_path = get_template_path(template)

    # 创建项目结构
    create_project_structure(project_name, template_path)

    print(f"项目 {project_name} 已成功创建！")
