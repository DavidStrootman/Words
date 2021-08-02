from abc import ABC


class PrintableABC(ABC):
    """Printable ABC Metaclass"""
    def __str__(self):
        return f"{self.__class__.__name__}"

    def __repr__(self):
        return self.__dict__
