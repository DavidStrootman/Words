from abc import ABC

from blocks.helper.token_type_enum import TokenTypeEnum


class Token(ABC):
    class Types(TokenTypeEnum):
        PLACEHOLDER = "PLACEHOLDER"

    def __init__(self, token_type: str):
        self.type = self.Types(token_type)


class DelimToken(Token):
    class Types(TokenTypeEnum):
        PAREN_OPEN = "("
        PAREN_CLOSE = ")"


class IdentToken(Token):
    class Types(TokenTypeEnum):
        IDENTIFIER = "IDENTIFIER"


class KeywordToken(Token):
    class Types(TokenTypeEnum):
        BEGIN = "BEGIN"
        WHILE = "WHILE"
        REPEAT = "REPEAT"
        IF = "IF"
        ELSE = "ELSE"
        THEN = "THEN"
        VARIABLE = "VARIABLE"
        VALUE = "VALUE"
        ASSIGN = "ASSIGN"
        RETURN = "RETURN"
        FUNCTION = "|"
        LAMBDA = "λ"


class LiteralToken(Token):
    class Types(TokenTypeEnum):
        NUMBER = "NUMBER"
        COMMENT = "#"


class MacroToken(Token):
    class Types(TokenTypeEnum):
        PRINT = "__PRINT__"


class OpToken(Token):
    class Types(TokenTypeEnum):
        MINUS = "-"
        PLUS = "+"
        EQUALS = "="
        GREATER = ">"
        LESSER = "<"
