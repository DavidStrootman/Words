from enum import Enum, unique
from typing import Tuple


@unique
class TokenTypeEnum(Enum):
    @classmethod
    def values(cls) -> Tuple[any, ...]:
        return tuple(value.value for value in cls.__members__.values())
