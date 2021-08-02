from abc import ABC, abstractmethod


class Debuggable(ABC):
    @abstractmethod
    def debug_str(self):
        pass
