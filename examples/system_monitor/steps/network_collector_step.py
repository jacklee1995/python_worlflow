import psutil
from typing import Dict, Any, List
from workflow_engine.interfaces.step_interface import StepInterface
from workflow_engine.interfaces.source_interface import SourceInterface
from workflow_engine.interfaces.output_interface import OutputInterface
from workflow_engine.interfaces.config_interface import ConfigInterface
import json
import asyncio

class NetworkCollectorStep(StepInterface):
    """
    网络收集步骤。

    收集网络接口的带宽使用情况和丢包率。
    """

    def __init__(self, name: str = 'NetworkCollectorStep', description: str = 'Collect network metrics'):
        self.name = name
        self.description = description
        self.config: ConfigInterface = None
        self.sources: List[SourceInterface] = []
        self.output: OutputInterface = None

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

        interval = self.config.get('interval', 5)
        interfaces = self.config.get('interfaces', [])

        while True:
            metrics = {}

            for interface in interfaces:
                net_io = psutil.net_io_counters(pernic=True).get(interface)
                if net_io:
                    metrics[interface] = {
                        'bytes_sent': net_io.bytes_sent,
                        'bytes_recv': net_io.bytes_recv,
                        'packets_sent': net_io.packets_sent,
                        'packets_recv': net_io.packets_recv,
                        'errin': net_io.errin,
                        'errout': net_io.errout,
                        'dropin': net_io.dropin,
                        'dropout': net_io.dropout
                    }

            # 输出收集到的指标
            await self.output.write(json.dumps(metrics, indent=2).encode())

            # 等待下一个采集周期
            await asyncio.sleep(interval) 