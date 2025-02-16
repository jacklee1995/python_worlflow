import argparse
from workflow.cli.commands.init_command import init_command
from workflow.cli.commands.run_command import run_command

def main():
    parser = argparse.ArgumentParser(description="Workflow CLI")
    subparsers = parser.add_subparsers(dest="command")

    # init 命令
    init_parser = subparsers.add_parser("init", help="初始化一个新的 Workflow 项目")
    init_parser.add_argument("project_name", nargs="?", help="项目名称")
    init_parser.add_argument("--template", default="project", help="使用的模板类型")

    # run 命令
    run_parser = subparsers.add_parser("run", help="运行任务")
    run_parser.add_argument("task_name", nargs="?", help="任务名称")
    run_parser.add_argument("--mode", default="development", help="运行模式")

    args = parser.parse_args()

    if args.command == "init":
        init_command(args.project_name, args.template)
    elif args.command == "run":
        run_command(args.task_name, args.mode)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
