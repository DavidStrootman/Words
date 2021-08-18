from abc import ABC, abstractmethod


class Debuggable(ABC):
    @abstractmethod
    def debug_str(self):
        """A debug string is used for providing better error messages during both parsing and at runtime."""
