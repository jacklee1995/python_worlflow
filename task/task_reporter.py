import os
from typing import List
from datetime import datetime

from intefaces.task import Task


class TaskReporter:
    """
    任务报告器。

    任务报告器负责生成任务执行报告，包括任务的状态、开始时间、结束时间和执行结果等信息。

    Attributes:
        report_dir (str): 报告文件的保存目录。

    Methods:
        set_report_dir(report_dir: str) -> None:
            设置报告文件的保存目录。

        generate_report(tasks: List[Task]) -> None:
            生成任务执行报告。

        _generate_task_report(task: Task) -> str:
            生成单个任务的执行报告。

        _save_report(report: str, filename: str) -> None:
            将报告内容保存到文件。
    """

    def __init__(self, report_dir: str = "reports"):
        """
        初始化 TaskReporter 实例。

        Args:
            report_dir (str): 报告文件的保存目录，默认为 "reports"。
        """
        self.report_dir = report_dir

    def set_report_dir(self, report_dir: str) -> None:
        """
        设置报告文件的保存目录。

        Args:
            report_dir (str): 报告文件的保存目录。

        Returns:
            None
        """
        self.report_dir = report_dir

    def generate_report(self, tasks: List[Task]) -> None:
        """
        生成任务执行报告。

        Args:
            tasks (List[Task]): 要生成报告的任务列表。

        Returns:
            None
        """
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"task_report_{timestamp}.txt"
        report_path = os.path.join(self.report_dir, report_filename)

        report_content = ""
        for task in tasks:
            task_report = self._generate_task_report(task)
            report_content += task_report + "\n\n"

        self._save_report(report_content, report_path)

    def _generate_task_report(self, task: Task) -> str:
        """
        生成单个任务的执行报告。

        Args:
            task (Task): 要生成报告的任务。

        Returns:
            str: 任务执行报告的内容。
        """
        report = f"Task Name: {task.name}\n"
        report += f"Task Description: {task.description}\n"
        report += f"Task Status: {task.get_status()}\n"
        report += f"Start Time: {task.get_start_time()}\n"
        report += f"End Time: {task.get_end_time()}\n"
        report += f"Steps:\n"

        for step in task.get_steps():
            report += f"  - {step.get_name()}: {step.get_description()}\n"

        return report

    def _save_report(self, report: str, filename: str) -> None:
        """
        将报告内容保存到文件。

        Args:
            report (str): 报告内容。
            filename (str): 报告文件名。

        Returns:
            None
        """
        with open(filename, "w") as file:
            file.write(report)
