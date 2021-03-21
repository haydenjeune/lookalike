from abc import ABC, abstractmethod


class Orchestrator(ABC):
    def __call__(self):
        self.run()

    @abstractmethod
    def run(self):
        pass