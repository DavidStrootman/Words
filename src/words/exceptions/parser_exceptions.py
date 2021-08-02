from words.helper.Debuggable import Debuggable


class StackSizeException(RuntimeError):
    def __init__(self, token: Debuggable, expected_size: int, actual_size: int):
        message = f"Got an incorrect stack size for {token.debug_str()}. Expected {expected_size}, got {actual_size}."
        super().__init__(message)
