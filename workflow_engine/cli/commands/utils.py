import shutil
from pathlib import Path

def prompt_user(prompt: str) -> str:
    """
    提示用户输入。

    Args:
        prompt (str): 提示信息。

    Returns:
        str: 用户输入的内容。
    """
    return input(prompt)

def create_project_structure(project_name: str, template_path: str):
    """
    创建项目结构。

    Args:
        project_name (str): 项目名称。
        template_path (str): 模板路径。
    """
    # 创建项目目录
    project_path = Path(project_name)
    project_path.mkdir(exist_ok=True)

    # 复制模板文件到项目目录
    shutil.copytree(template_path, project_path, dirs_exist_ok=True)

    # 替换项目名称
    replace_project_name(project_path, project_name)

def replace_project_name(project_path: Path, project_name: str):
    """
    替换项目名称。

    Args:
        project_path (Path): 项目路径。
        project_name (str): 项目名称。
    """
    # 替换 workflow.py 中的项目名称
    workflow_file = project_path / "workflow.py"
    if workflow_file.exists():
        with open(workflow_file, "r") as f:
            content = f.read()
        content = content.replace("{{project_name}}", project_name)
        with open(workflow_file, "w") as f:
            f.write(content) 