from abc import ABC


class PrintableABC(ABC):
    """Printable ABC."""
    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        return f"{str(self)}: {self.__dict__}"
