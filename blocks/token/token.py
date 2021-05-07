from abc import ABC, abstractmethod
from typing import Iterator, List, Optional, Type

from blocks.helper.token_type_enum import TokenTypeEnum
from blocks.parser.parse_util import eat_until, eat_until_discarding


class LexerToken(ABC):
    class Types(TokenTypeEnum):
        UNDEFINED = "UNDEFINED"

    def __init__(self, token_type: str):
        self.value = self.Types(token_type)

    @abstractmethod
    def parse(self, tokens: Iterator["LexerToken"]):
        pass


class ParserToken(ABC):
    """Base parser token."""


class WhileParserToken(ParserToken):
    def __init__(self, predicate: List[ParserToken], statements: List[ParserToken]):
        self.predicate = predicate
        self.statements = statements


class IfParserToken(ParserToken):
    def __init__(self, if_body: List[ParserToken], else_body: Optional[List[ParserToken]] = None):
        self.if_body = if_body
        self.else_body = else_body


class VariableParserToken(ParserToken):
    def __init__(self, value: str):
        self.value = value


class ValueParserToken(ParserToken):
    def __init__(self, value: str):
        self.value = value


class IdentParserToken(ParserToken):
    def __init__(self, value: str):
        self.value = value


class ReturnParserToken(ParserToken):
    def __init__(self, count: int):
        self.count = count

class FunctionParserToken(ParserToken):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters,
        self.body = body


class DelimLexerToken(LexerToken):
    class Types(TokenTypeEnum):
        PAREN_OPEN = "("
        PAREN_CLOSE = ")"

    def parse(self, tokens: Iterator["LexerToken"]):
        raise NotImplementedError("Tried to parse a delimiter token, this should be handled by its parent.")


class IdentLexerToken(LexerToken):
    def __init__(self, value: str):
        super().__init__("UNDEFINED")
        self.value = value

    def parse(self, tokens: Iterator["LexerToken"]):
        return IdentParserToken(self.value)


class KeywordLexerToken(LexerToken):
    class Types(TokenTypeEnum):
        BEGIN = "BEGIN"
        WHILE = "WHILE"
        REPEAT = "REPEAT"
        IF = "IF"
        ELSE = "ELSE"
        THEN = "THEN"
        VARIABLE = "VARIABLE"
        VALUE = "VALUE"
        RETURN = "RETURN"
        FUNCTION = "|"
        LAMBDA = "λ"

    def parse(self, tokens: Iterator["LexerToken"]):
        if self.value == self.Types.BEGIN:
            predicate = eat_until(tokens, self.Types.WHILE)
            predicate_without_last_item = predicate[:-1]
            statements = eat_until(tokens, self.Types.REPEAT)
            return WhileParserToken(predicate_without_last_item, statements)
        if self.value == self.Types.WHILE:
            raise NotImplementedError("Found unexpected WHILE token.")
        if self.value == self.Types.REPEAT:
            raise NotImplementedError("Found unexpected REPEAT token.")
        if self.value == self.Types.IF:
            if_body = eat_until(tokens, self.Types.ELSE)
            else_body = eat_until(tokens, self.Types.THEN)
            return IfParserToken(if_body, else_body)
        if self.value == self.Types.ELSE:
            raise NotImplementedError("Found unexpected ELSE token.")
        if self.value == self.Types.THEN:
            raise NotImplementedError("Tried to parse a THEN token, this should be handled by its IF token.")
        if self.value == self.Types.VARIABLE:
            return VariableParserToken(try_get_identifier_value(next(tokens)))
        if self.value == self.Types.VALUE:
            return ValueParserToken(try_get_identifier_value(next(tokens)))
        if self.value == self.Types.RETURN:
            return ReturnParserToken(try_get_return_value(next(tokens)))
        if self.value == self.Types.FUNCTION:
            token = next(tokens)
            if not isinstance(token, IdentLexerToken):
                raise RuntimeError(f"Expected IdentLexerToken, got {type(token)}")
            name = token.value
            paren_open = next(tokens)
            assert_type(paren_open, DelimLexerToken.Types.PAREN_OPEN)
            parameters = eat_until_discarding(tokens, DelimLexerToken.Types.PAREN_CLOSE)
            body = eat_until_discarding(tokens, KeywordLexerToken.Types.FUNCTION)
            return FunctionParserToken(name, parameters, body)
        if self.value == self.Types.LAMBDA:
            raise NotImplementedError("Lambdas not implemented yet")


def assert_instance_of(token, kind: Type[LexerToken]):
    if not isinstance(token, kind):
        raise RuntimeError(f"Expected {type(kind)} token, got {type(token)}.")


def assert_type(token, type_: TokenTypeEnum):
    if token.value is not type_:
        raise RuntimeError(f"Expected {type_} token, got {token.value}.")


def try_get_identifier_value(token):
    if not isinstance(token, IdentLexerToken):
        raise NotImplementedError(f"Expected IdentifierLexerToken, got {type(token)} with value \"{token.value}\".")
    return token.value


def try_get_return_value(token):
    if int(token.content) not in range(3):
        raise RuntimeError(f"Got too many return values ({token.value}), expected 0, 1 or 2")
    return int(token.content)


class LiteralLexerToken(LexerToken):
    class Types(TokenTypeEnum):
        NUMBER = "NUMBER"
        COMMENT = "#"

    def __init__(self, token_type, value):
        super().__init__(token_type)
        self.content = value

    def parse(self, tokens: Iterator["LexerToken"]):
        if self.value == self.Types.NUMBER:
            return NumberParserToken(self.content)


class NumberParserToken(ParserToken):
    def __init__(self, value: int):
        self.value = value


class MacroLexerToken(LexerToken):
    class Types(TokenTypeEnum):
        PRINT = "__PRINT__"

    def parse(self, tokens: Iterator["LexerToken"]):
        return MacroParserToken(self.value.value)


class MacroParserToken(ParserToken):
    def __init__(self, function_name: str):
        self.function_name = function_name


class OpLexerToken(LexerToken):
    class Types(TokenTypeEnum):
        SUBTRACTION = "-"
        ADDITION = "+"
        EQUALITY = "="
        GREATER = ">"
        LESSER = "<"
        GREATER_EQ = ">="
        LESER_EQ = ">="
        ASSIGNMENT = "ASSIGN"
        RETRIEVAL = "RETRIEVE"

    def parse(self, tokens: Iterator["LexerToken"]):
        if self.value.value in ["-", "+"]:
            return ArithmeticOperatorParserToken(self.value.value)
        if self.value.value in ["=", ">", "<", ">=", "<="]:
            return BooleanOperatorParserToken(self.value.value)
        if self.value.value in ["ASSIGN", "RETRIEVE"]:
            return DictionaryOperatorParserToken(self.value.value)


class ArithmeticOperatorParserToken(ParserToken):
    def __init__(self, value: str):
        self.value = value


class BooleanOperatorParserToken(ParserToken):
    def __init__(self, value: str):
        self.value = value


class DictionaryOperatorParserToken(ParserToken):
    def __init__(self, value: str):
        self.value = value
