from dataclasses import dataclass


@dataclass
class DebugData:
    """Holds data used during exception handling for debugging purposes."""
    line: int
    start_pos: int = None

    def __str__(self):
        return f"{self.line + 1}"


@dataclass
class Word:
    """Wrapper for a word holding the original lexed word and debug data."""
    content: str
    debug_data: DebugData
