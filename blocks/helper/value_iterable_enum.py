from enum import Enum, unique
from typing import Iterable

@unique
class ValueIterableEnum(Enum):
    @classmethod
    def values(cls) -> Iterable:
        yield from (value.value for value in cls.__members__.values())

