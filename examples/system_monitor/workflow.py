from workflow_engine.core.workflow import Workflow
from workflow_engine.core.workflow_registry import WorkflowRegistry
from workflow_engine.core.config import Config
from workflow_engine.sources import FileSource
from workflow_engine.core.output import Output
from workflow_engine.core.output_strategies.console_output_strategy import ConsoleOutputStrategy
from workflow_engine.core.output_strategies.file_output_strategy import FileOutputStrategy

from tasks.resource_monitor import monitor_system_resources
from tasks.log_analyzer import analyze_logs
from tasks.performance_reporter import generate_performance_report
from tasks.network_monitor import monitor_network
from tasks.security_audit import audit_security_logs

import sys
import os
import yaml
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class SystemMonitorWorkflow(Workflow):
    async def initialize(self):
        """初始化工作流"""
        # 加载配置
        with open('config/monitor_config.yaml', 'r', encoding='utf-8') as f:
            monitor_config_data = yaml.safe_load(f)
        with open('config/output_config.yaml', 'r', encoding='utf-8') as f:
            output_config_data = yaml.safe_load(f)

        monitor_config = Config(monitor_config_data)
        output_config = Config(output_config_data)

        # 创建数据源
        source = FileSource('config/monitor_config.yaml')
        source.set_config(monitor_config)

        # 创建输出
        console_output = None
        file_output = None

        # 配置控制台输出
        if output_config.get('outputs', {}).get('console', {}).get('enabled', False):
            console_strategy = ConsoleOutputStrategy()
            console_output = Output(console_strategy)

        # 配置文件输出
        if output_config.get('outputs', {}).get('file', {}).get('enabled', False):
            file_paths = output_config.get('outputs', {}).get('file', {}).get('paths', {})
            logs_path = os.path.join(os.getcwd(), file_paths.get('logs', 'outputs/logs'))
            os.makedirs(logs_path, exist_ok=True)
            
            resource_file_path = os.path.join(logs_path, 'resource_usage.json')
            file_strategy = FileOutputStrategy(resource_file_path)
            file_output = Output(file_strategy)

        # 创建任务
        resource_monitor_task = monitor_system_resources()
        log_analyzer_task = analyze_logs()
        performance_reporter_task = generate_performance_report()
        network_monitor_task = monitor_network()
        security_audit_task = audit_security_logs()

        # 设置任务的数据源和输出
        for task in [resource_monitor_task, network_monitor_task]:
            task.set_source(source)
            if console_output:
                task.set_output(console_output)
            if file_output:
                task.set_output(file_output)

        for task in [log_analyzer_task, performance_reporter_task, security_audit_task]:
            task.set_source(source)
            if file_output:
                task.set_output(file_output)

        # 添加任务
        await self.add_task(resource_monitor_task)
        await self.add_task(log_analyzer_task)
        await self.add_task(performance_reporter_task)
        await self.add_task(network_monitor_task)
        await self.add_task(security_audit_task)

# 注册工作流
WorkflowRegistry.register('system_monitor', SystemMonitorWorkflow) 

async def main():
    """主函数"""
    workflow = SystemMonitorWorkflow()
    await workflow.initialize()
    async for chunk in workflow.execute():
        pass  # 处理输出数据

if __name__ == "__main__":
    asyncio.run(main())