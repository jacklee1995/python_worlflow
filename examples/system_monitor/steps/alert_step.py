from typing import Dict, Any, List, Optional, AsyncIterator, Callable
from workflow_engine.interfaces.step_interface import StepInterface
from workflow_engine.interfaces.source_interface import SourceInterface
from workflow_engine.interfaces.output_interface import OutputInterface
from workflow_engine.interfaces.config_interface import ConfigInterface
import json
import asyncio

class AlertStep(StepInterface):
    """
    告警步骤。

    根据监控数据和配置中的阈值发送告警。
    """

    def __init__(self, name: str = 'AlertStep', description: str = 'Send alerts based on thresholds'):
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
        if not self.sources:
            raise ValueError("No sources provided")

        for source in self.sources:
            await source.open()
            try:
                async for data in source:
                    metrics = json.loads(data.decode())
                    alerts = self.check_alerts(metrics)
                    if alerts:
                        alert_message = json.dumps(alerts, indent=2)
                        await self.output.write(alert_message.encode())
            finally:
                await source.close()

    def check_alerts(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        alerts = []
        thresholds = self.config.get('thresholds', {})

        # 检查CPU使用率
        if metrics.get('cpu', {}).get('usage_percent', 0) > thresholds.get('cpu_usage', 80):
            alerts.append({
                'type': 'cpu',
                'message': f"High CPU usage: {metrics['cpu']['usage_percent']}%"
            })

        # 检查内存使用率
        if metrics.get('memory', {}).get('percent', 0) > thresholds.get('memory_usage', 85):
            alerts.append({
                'type': 'memory',
                'message': f"High memory usage: {metrics['memory']['percent']}%"
            })

        # 检查磁盘使用率
        if metrics.get('disk', {}).get('percent', 0) > thresholds.get('disk_usage', 90):
            alerts.append({
                'type': 'disk',
                'message': f"High disk usage: {metrics['disk']['percent']}%"
            })

        # 检查带宽使用率
        if metrics.get('network', {}).get('bandwidth_usage', 0) > thresholds.get('bandwidth_usage', 80):
            alerts.append({
                'type': 'network',
                'message': f"High bandwidth usage: {metrics['network']['bandwidth_usage']}%"
            })

        return alerts

    async def process(self, source: SourceInterface) -> AsyncIterator[bytes]:
        """处理输入流并生成输出流"""
        async for chunk in source:
            transformed = await self.transform(chunk)
            if self.output:
                metrics = json.loads(transformed.decode())
                alerts = self.check_alerts(metrics)
                if alerts:
                    alert_message = json.dumps(alerts, indent=2)
                    await self.output.write(alert_message.encode())
            yield transformed

    async def pipe(self, destination: 'StepInterface') -> 'StepInterface':
        """将当前步骤的输出连接到下一个步骤"""
        for handler in self._event_handlers['pipe']:
            handler(destination)
        
        async def process_and_pipe():
            if self.output:
                async for chunk in self.process(self.sources[0]):
                    await destination.get_output().write(chunk)
                    await destination.get_output().drain()
                await destination.get_output().write_eof()

        asyncio.create_task(process_and_pipe())
        return destination

    async def transform(self, chunk: bytes) -> bytes:
        """转换数据块"""
        return chunk

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