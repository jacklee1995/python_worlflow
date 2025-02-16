from typing import List, Union, IO
from workflow.interfaces.step_interface import StepInterface
from workflow.interfaces.source_interface import SourceInterface
from workflow.interfaces.destination_interface import DestinationInterface
from workflow.interfaces.config_interface import ConfigInterface

class Step(StepInterface):
    """
    步骤实现类，支持流式处理。
    """

    def __init__(self, name: str = 'Step', description: str = 'A workflow step'):
        self.name = name
        self.description = description
        self.config = None
        self.sources = []
        self.destination = None

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    def get_description(self) -> str:
        return self.description

    def set_description(self, description: str) -> None:
        self.description = description

    def set_config(self, config: ConfigInterface) -> None:
        self.config = config

    def get_config(self) -> ConfigInterface:
        return self.config

    def set_sources(self, sources: List[SourceInterface]) -> None:
        self.sources = sources

    def get_sources(self) -> List[SourceInterface]:
        return self.sources

    def set_destination(self, destination: DestinationInterface) -> None:
        self.destination = destination

    def get_destination(self) -> DestinationInterface:
        return self.destination

    def execute(self, input_stream: Union[IO, None] = None) -> IO:
        """
        执行步骤，支持流式处理。

        Args:
            input_stream (Union[IO, None]): 输入流。默认为 None。

        Returns:
            IO: 输出流。
        """
        raise NotImplementedError("Subclasses must implement execute()")

    def pipe(self, step: StepInterface) -> StepInterface:
        """
        将当前步骤的输出连接到下一个步骤的输入。

        Args:
            step (StepInterface): 下一个步骤。

        Returns:
            StepInterface: 下一个步骤。
        """
        output_stream = self.execute()
        step.set_sources([self.destination])
        step.execute(input_stream=output_stream)
        return step
