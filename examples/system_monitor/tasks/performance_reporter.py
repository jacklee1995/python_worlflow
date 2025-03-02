from workflow_engine.core.task import task
from workflow_engine.core.output import Output
from workflow_engine.core.config import Config
from workflow_engine.sources import FileSource
from workflow_engine.core.output_strategies.console_output_strategy import ConsoleOutputStrategy
from workflow_engine.core.output_strategies.file_output_strategy import FileOutputStrategy

from steps.report_generator_step import ReportGeneratorStep

@task
async def generate_performance_report(source: FileSource, output: Output) -> None:
    """性能报告生成任务"""

    # 加载配置
    config = source.get_config()
    report_config = config.get('performance_reporter', {})

    # 创建报告生成步骤
    report_generator_step = ReportGeneratorStep()
    report_generator_step.set_config(Config(report_config))

    # 设置数据源
    # 假设数据源是之前收集的资源使用数据
    data_source_path = 'outputs/logs/resource_usage.json'
    data_source = FileSource(data_source_path)
    report_generator_step.set_sources([data_source])

    # 设置输出
    output_config = config.get('outputs', {})
    console_output_enabled = output_config.get('console', {}).get('enabled', False)
    file_output_enabled = output_config.get('file', {}).get('enabled', False)

    if console_output_enabled:
        console_strategy = ConsoleOutputStrategy()
        console_output = Output(console_strategy)
        report_generator_step.set_output(console_output)

    if file_output_enabled:
        file_paths = output_config.get('file', {}).get('paths', {})
        report_file_path = file_paths.get('reports', 'outputs/reports/performance_report.html')
        file_strategy = FileOutputStrategy(report_file_path)
        file_output = Output(file_strategy)
        report_generator_step.set_output(file_output)

    # 如果没有启用任何输出,使用默认输出
    if not (console_output_enabled or file_output_enabled):
        report_generator_step.set_output(output)

    # 执行步骤
    await report_generator_step.execute() 