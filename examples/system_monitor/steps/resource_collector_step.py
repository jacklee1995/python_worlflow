import psutil
from typing import Dict, Any, List, Optional, AsyncIterator, Callable
from workflow_engine.core.step import Step
from workflow_engine.interfaces.source_interface import SourceInterface
from workflow_engine.interfaces.step_interface import StepInterface
import json
import asyncio
import signal
import time

class ResourceCollectorStep(Step):
    """
    资源收集步骤。

    收集系统资源使用情况，包括CPU、内存、磁盘和网络。
    """

    def __init__(self, name: str = 'ResourceCollectorStep', description: str = 'Collect system resource metrics'):
        super().__init__(name, description)
        self._running = True
        # 注册信号处理器
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """处理退出信号"""
        print("\nGracefully shutting down...")
        self._running = False

    async def execute(self) -> None:
        if not self.get_output():
            raise ValueError("Output not set")

        interval = self.get_config().get('interval', 5)
        run_duration = self.get_config().get('run_duration', 60)  # 默认运行60秒
        start_time = time.time()

        try:
            while self._running:
                # 检查是否超过运行时间
                if time.time() - start_time > run_duration:
                    print("\nMonitoring duration completed.")
                    break

                # 收集并输出指标
                metrics = await self.collect_metrics()
                if metrics and self.get_output():
                    await self.get_output().write(json.dumps(metrics, indent=2).encode())

                # 等待下一个采集周期，但支持中断
                try:
                    await asyncio.sleep(interval)
                except asyncio.CancelledError:
                    break

        except Exception as e:
            print(f"Error during execution: {e}")
            raise
        finally:
            # 确保优雅关闭
            if self.get_output():
                await self.get_output().close()
            print("Monitoring stopped.")

    async def process(self, source: SourceInterface) -> AsyncIterator[bytes]:
        """处理输入流并生成输出流"""
        # 确保源文件已打开
        await source.open()
        try:
            async for chunk in source:
                transformed = await self.transform(chunk)
                # 不要直接写入源数据到输出
                yield transformed
        finally:
            await source.close()

    async def pipe(self, destination: 'StepInterface') -> 'StepInterface':
        """将当前步骤的输出连接到下一个步骤"""
        for handler in self._event_handlers['pipe']:
            handler(destination)
        
        async def process_and_pipe():
            if self.get_output() and self.get_sources():
                # 确保源文件已打开
                await self.get_sources()[0].open()
                try:
                    # 不要处理源文件数据，而是直接使用收集到的指标
                    metrics = await self.collect_metrics()
                    if metrics:
                        await destination.get_output().write(json.dumps(metrics, indent=2).encode())
                finally:
                    await self.get_sources()[0].close()

        asyncio.create_task(process_and_pipe())
        return destination

    async def collect_metrics(self) -> Dict[str, Any]:
        """收集系统指标"""
        metrics_config = self.get_config().get('metrics', {})
        metrics = {}

        # 收集CPU信息
        if metrics_config.get('cpu'):
            metrics['cpu'] = {
                'usage_percent': psutil.cpu_percent(interval=1)
            }

        # 收集内存信息
        if metrics_config.get('memory'):
            mem = psutil.virtual_memory()
            metrics['memory'] = {
                'total': mem.total,
                'available': mem.available,
                'percent': mem.percent
            }

        # 收集磁盘信息
        if metrics_config.get('disk'):
            disk = psutil.disk_usage('/')
            metrics['disk'] = {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent
            }

        # 收集网络信息
        if metrics_config.get('network'):
            net_io = psutil.net_io_counters()
            metrics['network'] = {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv
            }

        return metrics

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