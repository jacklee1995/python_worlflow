import os
import asyncio
from typing import Dict, Any
import json
import csv
from io import StringIO

from workflow_engine.core.config import Config
from workflow_engine.core.loader import Loader
from workflow_engine.core.output import Output
from workflow_engine.sources import FileSource
from workflow_engine.core.task import task
from workflow_engine.core.workflow import Workflow
from workflow_engine.core.output_strategies.console_output_strategy import ConsoleOutputStrategy
from workflow_engine.steps.aggregate_step import AggregateStep
from workflow_engine.steps.transform_step import TransformStep


@task
async def analyze_sales(source: FileSource, output: Output) -> None:
    """分析销售数据的任务"""
    
    # 创建步骤
    aggregate_step = AggregateStep()
    aggregate_step.set_aggregation_functions({
        "sales": sum,
        "quantity": sum,
        "price": "mean"
    })

    def transform_func(data: bytes) -> Dict[str, Any]:
        # 将字节串解码为 UTF-8 字符串
        csv_data = data.decode('utf-8')
        
        # 使用 csv 模块解析 CSV 数据
        reader = csv.DictReader(StringIO(csv_data))
        for row in reader:
            # 计算每行的 total
            row["total"] = float(row["price"]) * float(row["quantity"])
            # 输出每行的结果
            output.write(json.dumps(row, indent=2).encode())
        
        return row  # 返回最后一行数据

    transform_step = TransformStep(transform_func)

    # 设置数据源和输出
    aggregate_step.set_sources([source])
    aggregate_step.set_output(output)
    transform_step.set_output(output)
    
    # 使用 pipe 连接步骤
    await aggregate_step.pipe(transform_step)
    
    # 执行步骤
    async for data in aggregate_step.execute():
        # 数据已经通过 pipe 传递给了 transform_step
        pass


async def main():
    # 获取脚本文件所在的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 计算项目根目录
    project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))

    # 创建配置对象,指定 base_dir 为项目根目录
    config = Config(base_dir=project_root)
    config.set("input_path", "examples/basic_workflow/data/input.csv")
    config.set("output_path", "examples/basic_workflow/data/output.txt")

    # 创建加载器
    loader = Loader()

    # 创建文件数据源
    source = FileSource(config.get("input_path"))

    # 创建输出
    output_strategy = ConsoleOutputStrategy()
    output = Output(output_strategy)

    # 创建工作流
    workflow = Workflow("SalesWorkflow", "A workflow to analyze sales data")
    
    # 创建并添加任务
    sales_task = analyze_sales()
    sales_task.set_source(source)
    sales_task.set_output(output)
    await workflow.add_task(sales_task)

    # 设置工作流配置
    workflow.set_config(config)

    # 执行工作流
    async for _ in workflow.execute():
        pass

    # 关闭输出
    await output.close()


if __name__ == "__main__":
    asyncio.run(main()) 