from words.helper.Debuggable import Debuggable
from words.helper.TokenTypeEnum import TokenTypeEnum
from typing import Type


class UnexpectedTokenError(SyntaxError):
    """An unexpected token error is raised whenever a specific token is expected, but not found."""
    def __init__(self, actual_token: Debuggable, expected_token: Type[Debuggable]):
        message = f"Expected {expected_token}, got {actual_token.debug_str()}"
        super().__init__(message)


class UnexpectedTokenTypeError(SyntaxError):
    """An unexpected token type error is raised whenever a specific token type is expected, but not found."""
    def __init__(self, actual_token: Debuggable, expected_type: TokenTypeEnum):
        message = f"Expected a token of type {expected_type}, got {actual_token.debug_str()}"
        super().__init__(message)


class InvalidTokenError(SyntaxError):
    """An invalid token error is raised when a token is placed in an invalid location in the code."""
    def __init__(self, token: Debuggable):
        message = f"Got an invalid token {token.debug_str()}."
        super().__init__(message)


class IncorrectReturnCountError(SyntaxError):
    def __init__(self, token: Debuggable):
        message = f"Got too many return values: {token.debug_str()}, expected 0, 1 or 2"
        super().__init__(message)