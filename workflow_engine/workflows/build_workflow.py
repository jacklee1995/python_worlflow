from workflow_engine.core.workflow import Workflow
from workflow_engine.core.task import task
from workflow_engine.core.step import Step

# 定义步骤
class CleanStep(Step):
    def execute(self, input_stream=None):
        print("Cleaning build directory...")
        return "Cleaned"

class CompileStep(Step):
    def execute(self, input_stream=None):
        print("Compiling code...")
        return "Compiled"

class TestStep(Step):
    def execute(self, input_stream=None):
        print("Running tests...")
        return "Tests passed"

# 定义任务
@task
def build_task():
    clean_step = CleanStep(name="Clean")
    compile_step = CompileStep(name="Compile")
    test_step = TestStep(name="Test")

    # 串联执行步骤
    build_task.series(clean_step, compile_step, test_step)

# 定义工作流
class BuildWorkflow(Workflow):
    def __init__(self):
        super().__init__(name="Build and Test Workflow")
        self.add_task(build_task)

# 注册工作流
from workflow_engine.core.workflow_registry import WorkflowRegistry
WorkflowRegistry.register('build', BuildWorkflow) 