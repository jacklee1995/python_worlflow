from workflow_engine.core.task import task
from workflow_engine.core.output import Output
from workflow_engine.core.config import Config
from workflow_engine.sources import FileSource
from workflow_engine.core.output_strategies.console_output_strategy import ConsoleOutputStrategy
from workflow_engine.core.output_strategies.file_output_strategy import FileOutputStrategy
import os

from steps.resource_collector_step import ResourceCollectorStep
from steps.alert_step import AlertStep

@task
async def monitor_system_resources(source: FileSource, output: Output) -> None:
    """系统资源监控任务"""

    # 加载配置
    config = source.get_config()
    monitor_config = config.get('resource_monitor', {})
    
    # 创建输出目录
    output_config = config.get('outputs', {})
    if output_config.get('file', {}).get('enabled', False):
        file_paths = output_config.get('file', {}).get('paths', {})
        for path in file_paths.values():
            os.makedirs(path, exist_ok=True)

    # 创建资源收集步骤
    resource_collector_step = ResourceCollectorStep()
    resource_collector_step.set_config(Config(monitor_config))

    # 创建告警步骤
    alert_step = AlertStep()
    alert_step.set_config(Config(monitor_config))

    # 设置输出
    output_config = config.get('outputs', {})
    console_output_enabled = output_config.get('console', {}).get('enabled', False)
    file_output_enabled = output_config.get('file', {}).get('enabled', False)

    # 设置资源收集步骤的输出
    if console_output_enabled:
        console_strategy = ConsoleOutputStrategy()
        console_output = Output(console_strategy)
        resource_collector_step.set_output(console_output)

    if file_output_enabled:
        file_paths = output_config.get('file', {}).get('paths', {})
        resource_file_path = file_paths.get('logs', 'outputs/logs/resource_usage.json')
        file_strategy = FileOutputStrategy(resource_file_path, append=False)
        file_output = Output(file_strategy)
        resource_collector_step.set_output(file_output)

    # 如果没有启用任何输出，使用默认输出
    if not (console_output_enabled or file_output_enabled):
        resource_collector_step.set_output(output)

    # 设置告警步骤的输出
    alert_step.set_output(output)

    # 设置数据源
    resource_collector_step.set_sources([source])
    alert_step.set_sources([source])

    # 连接步骤
    await resource_collector_step.pipe(alert_step)

    # 执行步骤
    await resource_collector_step.execute() 