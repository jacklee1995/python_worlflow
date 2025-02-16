from workflow import task, series, parallel, watch, src, dest, env
from workflow.loaders.yaml_task_loader import YamlTaskLoader
from workflow.steps.watch_step import WatchStep
from src.loaders.image_loader import ImageLoader

# 加载 YAML 任务
yaml_loader = YamlTaskLoader()
build_task = yaml_loader.create_task(yaml_loader.load('workflows/build.yaml'))

image_loader = ImageLoader()
image_source = image_loader.load('assets/images/logo.png')

@task
def watch_files():
    watch_step = WatchStep()
    watch_step.set_sources([src('src/**/*')])
    watch_step.on_change(lambda: build_task())
    watch_step.execute()

@task
def default():
    return series(build_task, watch_files) 