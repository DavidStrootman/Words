from words.helper.Debuggable import Debuggable


class StackSizeException(RuntimeError):
    def __init__(self, token: Debuggable, expected_size: int, actual_size: int):
        message = f"Got an incorrect stack size for {token.debug_str()}. Expected {expected_size}, got {actual_size}."
        super().__init__(message)


class InvalidPredicateException(RuntimeError):
    """An invalid predicate exception is raised whenever the result of a predicate is not of type boolean."""
    def __init__(self, token: Debuggable):
        message = f"Got a non-boolean value as a predicate of {token.debug_str()}."
        super().__init__(message)


class UndefinedIdentifierException(NameError):
    """An undefined identifier exception is raised whenever an identifier is used, that was not (yet) defined."""
    def __init__(self, token: Debuggable):
        message = f"Undefined function or variable, {token.debug_str()}."
        super().__init__(message)
