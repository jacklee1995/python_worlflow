from workflow.core.task import task
from workflow.core.step import Step
from workflow.core.source import Source
from workflow.core.destination import Destination
from workflow.core.config import Config

@task
def build():
    src = Source('src/**/*.js')
    dest = Destination('dist/js/')
    step1 = Step(name='Step1', description='Process JS files')
    step2 = Step(name='Step2', description='Minify JS files')

    src.pipe(step1).pipe(step2).pipe(dest)

if __name__ == '__main__':
    config = Config({'output_dir': 'dist'})
    build_task = build()
    build_task.set_config(config)
    build_task.execute() 