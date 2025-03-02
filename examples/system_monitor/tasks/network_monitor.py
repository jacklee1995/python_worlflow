from workflow_engine.core.task import task
from workflow_engine.core.output import Output
from workflow_engine.core.config import Config
from workflow_engine.sources import FileSource
from workflow_engine.core.output_strategies.console_output_strategy import ConsoleOutputStrategy
from workflow_engine.core.output_strategies.file_output_strategy import FileOutputStrategy

from steps.alert_step import AlertStep
from steps.network_collector_step import NetworkCollectorStep

@task
async def monitor_network(source: FileSource, output: Output) -> None:
    """网络监控任务"""

    # 加载配置
    config = source.get_config()
    network_config = config.get('network_monitor', {})

    # 创建网络收集步骤
    network_collector_step = NetworkCollectorStep()
    network_collector_step.set_config(Config(network_config))

    # 创建告警步骤
    alert_step = AlertStep()
    alert_step.set_config(Config(network_config))

    # 设置输出
    output_config = config.get('outputs', {})
    console_output_enabled = output_config.get('console', {}).get('enabled', False)
    file_output_enabled = output_config.get('file', {}).get('enabled', False)

    if console_output_enabled:
        console_strategy = ConsoleOutputStrategy()
        console_output = Output(console_strategy)
        # network_collector_step.set_output(console_output)
        alert_step.set_output(console_output)

    if file_output_enabled:
        file_paths = output_config.get('file', {}).get('paths', {})
        network_file_path = file_paths.get('logs', 'outputs/logs/network_usage.json')
        file_strategy = FileOutputStrategy(network_file_path, append=False)
        file_output = Output(file_strategy)
        network_collector_step.set_output(file_output)
        alert_step.set_output(file_output)

    # 连接步骤
    await network_collector_step.pipe(alert_step)

    # 执行步骤
    await network_collector_step.execute() 