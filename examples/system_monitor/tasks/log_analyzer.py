from workflow_engine.core.task import task
from workflow_engine.core.output import Output
from workflow_engine.core.config import Config
from workflow_engine.sources import FileSource
from workflow_engine.core.output_strategies.console_output_strategy import ConsoleOutputStrategy
from workflow_engine.core.output_strategies.file_output_strategy import FileOutputStrategy

from steps.log_parser_step import LogParserStep

@task
async def analyze_logs(source: FileSource, output: Output) -> None:
    """日志分析任务"""

    # 加载配置
    config = source.get_config()
    log_config = config.get('log_analyzer', {})

    # 创建日志解析步骤
    log_parser_step = LogParserStep()
    log_parser_step.set_config(Config(log_config))

    # 设置数据源
    log_paths = log_config.get('log_paths', [])
    sources = [FileSource(path) for path in log_paths]
    log_parser_step.set_sources(sources)

    # 设置输出
    output_config = config.get('outputs', {})
    console_output_enabled = output_config.get('console', {}).get('enabled', False)
    file_output_enabled = output_config.get('file', {}).get('enabled', False)

    # 如果没有启用任何输出，使用默认输出
    if not (console_output_enabled or file_output_enabled):
        log_parser_step.set_output(output)
        return

    if console_output_enabled:
        console_strategy = ConsoleOutputStrategy()
        console_output = Output(console_strategy)
        log_parser_step.set_output(console_output)

    if file_output_enabled:
        file_paths = output_config.get('file', {}).get('paths', {})
        log_file_path = file_paths.get('logs', 'outputs/logs/log_analysis.json')
        file_strategy = FileOutputStrategy(log_file_path, append=False)  # 设置为不追加模式
        file_output = Output(file_strategy)
        log_parser_step.set_output(file_output)

    # 执行步骤
    await log_parser_step.execute() 