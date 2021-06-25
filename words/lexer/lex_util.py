from dataclasses import dataclass


@dataclass
class DebugData:
    line: int
    start_pos: int = None


@dataclass
class Word:
    content: str
    debug_data: DebugData
