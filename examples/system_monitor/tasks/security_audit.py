from workflow_engine.core.task import task
from workflow_engine.core.output import Output
from workflow_engine.core.config import Config
from workflow_engine.sources import FileSource
from workflow_engine.core.output_strategies.console_output_strategy import ConsoleOutputStrategy
from workflow_engine.core.output_strategies.file_output_strategy import FileOutputStrategy

from steps.log_parser_step import LogParserStep
from steps.alert_step import AlertStep

@task
async def audit_security_logs(source: FileSource, output: Output) -> None:
    """安全审计任务"""

    # 加载配置
    config = source.get_config()
    audit_config = config.get('security_audit', {})

    # 创建日志解析步骤
    log_parser_step = LogParserStep()
    log_parser_step.set_config(Config(audit_config))

    # 创建告警步骤
    alert_step = AlertStep()
    alert_step.set_config(Config(audit_config))

    # 设置数据源
    audit_paths = audit_config.get('audit_paths', [])
    sources = [FileSource(path) for path in audit_paths]
    log_parser_step.set_sources(sources)

    # 设置输出
    output_config = config.get('outputs', {})
    console_output_enabled = output_config.get('console', {}).get('enabled', False)
    file_output_enabled = output_config.get('file', {}).get('enabled', False)

    if console_output_enabled:
        console_strategy = ConsoleOutputStrategy()
        console_output = Output(console_strategy)
        log_parser_step.set_output(console_output)
        alert_step.set_output(console_output)

    if file_output_enabled:
        file_paths = output_config.get('file', {}).get('paths', {})
        audit_file_path = file_paths.get('logs', 'outputs/logs/security_audit.json')
        file_strategy = FileOutputStrategy(audit_file_path)
        file_output = Output(file_strategy)
        log_parser_step.set_output(file_output)
        alert_step.set_output(file_output)

    # 连接步骤
    await log_parser_step.pipe(alert_step)

    # 执行步骤
    await log_parser_step.execute() 