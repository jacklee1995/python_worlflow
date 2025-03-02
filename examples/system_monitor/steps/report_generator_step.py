from typing import Dict, Any, List, Optional, AsyncIterator, Callable
from workflow_engine.interfaces.step_interface import StepInterface
from workflow_engine.interfaces.source_interface import SourceInterface
from workflow_engine.interfaces.output_interface import OutputInterface
from workflow_engine.interfaces.config_interface import ConfigInterface
import json
import datetime
import asyncio
import os

class ReportGeneratorStep(StepInterface):
    """
    报告生成步骤。

    根据收集到的系统资源数据生成性能报告。
    """

    def __init__(self, name: str = 'ReportGeneratorStep', description: str = 'Generate performance reports'):
        self.name = name
        self.description = description
        self.config: ConfigInterface = None
        self.sources: List[SourceInterface] = []
        self.output: OutputInterface = None
        self._event_handlers: Dict[str, List[Callable]] = {
            'data': [],
            'error': [],
            'end': [],
            'pipe': []
        }

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    def get_description(self) -> str:
        return self.description

    def set_description(self, description: str) -> None:
        self.description = description

    def set_config(self, config: ConfigInterface) -> None:
        self.config = config

    def get_config(self) -> ConfigInterface:
        return self.config

    def set_sources(self, sources: List[SourceInterface]) -> None:
        self.sources = sources

    def get_sources(self) -> List[SourceInterface]:
        return self.sources

    def set_output(self, output: OutputInterface) -> None:
        self.output = output

    def get_output(self) -> OutputInterface:
        return self.output

    async def execute(self) -> None:
        if not self.output:
            raise ValueError("Output not set")

        report_config = self.config.get('report', {})
        sections = report_config.get('sections', [])
        report_format = report_config.get('format', 'text')

        # 从数据源读取数据
        data = {}
        for source in self.sources:
            await source.open()  # 打开数据源
            try:
                async for chunk in source.read_chunks():
                    data.update(json.loads(chunk))
            finally:
                await source.close()  # 关闭数据源

        # 生成报告
        report = self.generate_report(data, sections, report_format)

        # 输出报告
        await self.output.write(report.encode())

    def generate_report(self, data: Dict[str, Any], sections: List[str], report_format: str) -> str:
        report = f"Performance Report ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n\n"
        report += "=" * 50 + "\n"

        if 'resource_usage' in sections:
            report += self.generate_resource_usage_section(data)

        if 'error_summary' in sections:
            report += self.generate_error_summary_section(data)

        if 'performance_metrics' in sections:
            report += self.generate_performance_metrics_section(data)

        if report_format == 'html':
            report = self.convert_to_html(report)
        elif report_format == 'pdf':
            report = self.convert_to_pdf(report)

        return report

    def generate_resource_usage_section(self, data: Dict[str, Any]) -> str:
        section = "Resource Usage:\n"
        section += "-" * 20 + "\n"
        for resource, values in data.items():
            section += f"{resource.capitalize()}:\n"
            for value in values:
                section += f"  {value}\n"
        section += "\n"
        return section

    def generate_error_summary_section(self, data: Dict[str, Any]) -> str:
        # Placeholder for error summary generation
        return "Error Summary:\n" + "-" * 20 + "\nNo errors detected.\n\n"

    def generate_performance_metrics_section(self, data: Dict[str, Any]) -> str:
        # Placeholder for performance metrics generation
        return "Performance Metrics:\n" + "-" * 20 + "\nMetrics not available.\n\n"

    def convert_to_html(self, report: str) -> str:
        # Placeholder for HTML conversion
        return f"<html><body><pre>{report}</pre></body></html>"

    def convert_to_pdf(self, report: str) -> str:
        # Placeholder for PDF conversion
        return report  # In a real implementation, this would convert the report to PDF format

    async def process(self, source: SourceInterface) -> AsyncIterator[bytes]:
        """处理数据源"""
        async for chunk in source:
            transformed = await self.transform(chunk)
            yield transformed

    async def transform(self, chunk: bytes) -> bytes:
        """转换数据块"""
        return chunk

    async def pipe(self, destination: 'StepInterface') -> 'StepInterface':
        """将当前步骤的输出连接到下一个步骤"""
        for handler in self._event_handlers['pipe']:
            handler(destination)

        async def process_and_pipe():
            async for chunk in self.process(self.sources[0]):
                await destination.get_output().write(chunk)
                await destination.get_output().drain()
            await destination.get_output().write_eof()

        asyncio.create_task(process_and_pipe())
        return destination

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