from enum import Enum, unique
from typing import Tuple


@unique
class TokenTypeEnum(Enum):
    @classmethod
    def values(cls) -> Tuple[any, ...]:
        return tuple(map(lambda value: value.value, cls.__members__.values()))
