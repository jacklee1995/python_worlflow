import os
import json
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, AsyncIterator
import asyncio

from workflow_engine.interfaces.output_strategy import OutputStrategy
from workflow_engine.interfaces.output_types import OutputErrorType, RetryPolicy, OutputMetrics

class SystemMonitorReportOutputStrategy(OutputStrategy):
    """
    系统监控报告输出策略,用于生成和保存系统监控报告。
    报告格式为 HTML,包含系统资源使用情况的图表和统计信息。
    """

    def __init__(self, report_path: str, report_title: str = "System Monitor Report"):
        """
        初始化系统监控报告输出策略。

        Args:
            report_path (str): 报告文件路径
            report_title (str): 报告标题,默认为 "System Monitor Report"
        """
        self.report_path = report_path
        self.report_title = report_title
        self._file = None
        self._metrics = OutputMetrics()
        self._retry_policy = RetryPolicy()
        self._event_handlers = {
            'data': [],
            'error': [],
            'close': []
        }

    async def open(self) -> None:
        """打开报告文件并写入 HTML 头部"""
        os.makedirs(os.path.dirname(self.report_path), exist_ok=True)
        self._file = open(self.report_path, 'w', encoding='utf-8')
        await self._write_html_header()

    async def _write_html_header(self) -> None:
        """写入 HTML 头部"""
        header = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{self.report_title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                h1 {{ color: #333; }}
                .chart-container {{ margin: 20px 0; }}
                .statistics {{ margin-top: 30px; }}
            </style>
        </head>
        <body>
            <h1>{self.report_title}</h1>
        """
        self._file.write(header)

    async def write(self, data: Dict[str, Any]) -> None:
        """
        将系统监控数据写入报告。
        数据格式应为包含 CPU、内存、磁盘等使用情况的字典。

        Args:
            data (Dict[str, Any]): 系统监控数据
        """
        if not self._file:
            await self.open()

        try:
            # 将数据转换为 HTML 内容
            html_content = self._generate_html_content(data)
            self._file.write(html_content)
            self._metrics.bytes_written += len(html_content.encode('utf-8'))
        except Exception as e:
            self._metrics.error_count += 1
            await self.handle_error(e)

    def _generate_html_content(self, data: Dict[str, Any]) -> str:
        """
        生成 HTML 内容,包含图表和统计信息。

        Args:
            data (Dict[str, Any]): 系统监控数据

        Returns:
            str: 生成的 HTML 内容
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        html = f"""
        <div class="chart-container">
            <h2>Resource Usage at {timestamp}</h2>
            <div id="chart-{timestamp}" style="width: 100%; height: 400px;"></div>
        </div>
        <div class="statistics">
            <h3>Statistics</h3>
            <ul>
                <li>CPU Usage: {data.get('cpu', {}).get('usage_percent', 0)}%</li>
                <li>Memory Usage: {data.get('memory', {}).get('percent', 0)}%</li>
                <li>Disk Usage: {data.get('disk', {}).get('percent', 0)}%</li>
            </ul>
        </div>
        """
        return html

    async def close(self) -> None:
        """关闭报告文件并写入 HTML 尾部"""
        if self._file:
            await self._write_html_footer()
            self._file.close()

    async def _write_html_footer(self) -> None:
        """写入 HTML 尾部"""
        footer = """
        </body>
        </html>
        """
        self._file.write(footer)

    async def handle_error(self, error: Exception) -> None:
        """处理错误"""
        error_type = OutputErrorType.FILE_SYSTEM_ERROR
        self._metrics.error_count += 1
        for handler in self._event_handlers['error']:
            handler(error)
        raise error

    def get_metrics(self) -> OutputMetrics:
        """获取输出指标"""
        return self._metrics

    def clear_metrics(self) -> None:
        """清除输出指标"""
        self._metrics = OutputMetrics()

    def get_retry_policy(self) -> RetryPolicy:
        """获取重试策略"""
        return self._retry_policy

    def set_retry_policy(self, policy: RetryPolicy) -> None:
        """设置重试策略"""
        self._retry_policy = policy

    def on(self, event: str, callback: Callable) -> None:
        """注册事件处理器"""
        if event not in self._event_handlers:
            raise ValueError(f"Unsupported event: {event}")
        self._event_handlers[event].append(callback)

    def off(self, event: str, callback: Optional[Callable] = None) -> None:
        """移除事件处理器"""
        if event not in self._event_handlers:
            raise ValueError(f"Unsupported event: {event}")
        if callback is None:
            self._event_handlers[event].clear()
        else:
            self._event_handlers[event] = [
                h for h in self._event_handlers[event] if h != callback
            ] 