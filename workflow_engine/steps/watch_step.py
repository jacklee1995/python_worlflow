import time
import os
from typing import List, Callable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from workflow_engine.interfaces.step_interface import StepInterface
from workflow_engine.interfaces.source_interface import SourceInterface
from workflow_engine.interfaces.config_interface import ConfigInterface

class WatchStep(StepInterface):
    """
    监听步骤。
    
    用于监听文件变化并触发相应的任务。
    """

    def __init__(self, name: str = 'WatchStep', description: str = 'Watch files for changes'):
        self.name = name
        self.description = description
        self.config = None
        self.sources = []
        self.callbacks: List[Callable] = []
        self.observer = Observer()

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

    def on_change(self, callback: Callable) -> None:
        """
        注册文件变化时的回调函数。

        Args:
            callback (Callable): 回调函数。
        """
        self.callbacks.append(callback)

    def execute(self) -> None:
        """
        开始监听文件变化。
        """
        class EventHandler(FileSystemEventHandler):
            def __init__(self, callbacks):
                self.callbacks = callbacks

            def on_modified(self, event):
                for callback in self.callbacks:
                    callback()

        for source in self.sources:
            if source.is_dir():
                self.observer.schedule(EventHandler(self.callbacks), source.get_path(), recursive=True)
            elif source.is_file():
                self.observer.schedule(EventHandler(self.callbacks), os.path.dirname(source.get_path()), recursive=False)

        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def pipe(self, step: StepInterface) -> StepInterface:
        """
        将当前步骤的输出连接到另一个步骤的输入。

        Args:
            step (StepInterface): 下一个步骤。

        Returns:
            StepInterface: 下一个步骤。
        """
        return step 