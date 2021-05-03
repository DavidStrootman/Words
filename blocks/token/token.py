from typing import TypeVar

from blocks.helper.value_iterable_enum import ValueIterableEnum


class MacroType(ValueIterableEnum):
    PRINT = "__PRINT__"


class TokenType(ValueIterableEnum):
    BEGIN = "BEGIN"
    WHILE = "WHILE"
    REPEAT = "REPEAT"
    IF = "IF"
    ELSE = "ELSE"
    THEN = "THEN"
    VARIABLE = "VARIABLE"
    ASSIGN = "ASSIGN"
    FUNC = "|"
    LAMB = "λ"
    PAREN_OPEN = "("
    PAREN_CLOSE = ")"
    MINUS = "-"
    PLUS = "+"
    EQUALS = "="
    GREATER = ">"
    LESSER = "<"
    COMMENT = "#"
    NUMBER = "NUMBER"
    LITERAL = "LITERAL"


TokenTyping = TypeVar("TokenTyping", MacroType, TokenType)


class Token:
    """Base Token"""
    def __init__(self, token_type):
        self.type: TokenTyping = token_type
