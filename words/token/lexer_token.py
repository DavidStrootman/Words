from abc import ABC, abstractmethod
from typing import Iterator, Type

from words.helper.token_type_enum import TokenTypeEnum
from words.lexer.lex_util import Word
from words.parser.parse_util import eat_until, eat_until_discarding
from words.token.parser_token import DictionaryOperatorParserToken, BooleanOperatorParserToken, \
    ArithmeticOperatorParserToken, BooleanParserToken, MacroParserToken, NumberParserToken, FunctionParserToken, ReturnParserToken, \
    ValueParserToken, VariableParserToken, IdentParserToken, IfParserToken, WhileParserToken


class LexerToken(ABC):
    class Types(TokenTypeEnum):
        UNDEFINED = "UNDEFINED"

    def __init__(self, word: Word):
        self.debug_data = word.debug_data
        self.value = self.Types(word.content)

    @abstractmethod
    def parse(self, tokens: Iterator["LexerToken"]):
        pass

    @staticmethod
    def assert_instance_of(token, kind: Type["LexerToken"]):
        if not isinstance(token, kind):
            raise RuntimeError(f"Expected {kind} token, got {type(token)}.")

    @staticmethod
    def assert_type(token, type_: TokenTypeEnum):
        if token.value is not type_:
            raise RuntimeError(f"Expected {type_} token, got {token.value}.")

    @staticmethod
    def try_get_identifier_value(token):
        if not isinstance(token, IdentLexerToken):
            raise NotImplementedError(f"Expected IdentifierLexerToken, got {type(token)} with value \"{token.value}\".")
        return token.value

    @staticmethod
    def try_get_return_value(token):
        LexerToken.assert_instance_of(token, LiteralLexerToken)
        if int(token.content) not in range(3):
            raise RuntimeError(f"Got too many return values ({token.value}), expected 0, 1 or 2")
        return int(token.content)


class DelimLexerToken(LexerToken):
    class Types(TokenTypeEnum):
        PAREN_OPEN = "("
        PAREN_CLOSE = ")"

    def parse(self, tokens: Iterator["LexerToken"]):
        raise NotImplementedError("Tried to parse a delimiter token, this should be handled by its parent.")


class IdentLexerToken(LexerToken):
    def __init__(self, word: Word):
        super().__init__(Word("UNDEFINED", word.debug_data))
        self.value = word.content

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
            statements = eat_until_discarding(tokens, self.Types.REPEAT)
            return WhileParserToken(predicate_without_last_item, statements)
        if self.value == self.Types.WHILE:
            raise NotImplementedError("Found unexpected WHILE token.")
        if self.value == self.Types.REPEAT:
            raise NotImplementedError("Found unexpected REPEAT token.")
        if self.value == self.Types.IF:
            if_body = eat_until_discarding(tokens, self.Types.ELSE)
            else_body = eat_until_discarding(tokens, self.Types.THEN)
            return IfParserToken(if_body, else_body)
        if self.value == self.Types.ELSE:
            raise NotImplementedError("Found unexpected ELSE token.")
        if self.value == self.Types.THEN:
            raise NotImplementedError("Tried to parse a THEN token, this should be handled by its IF token.")
        if self.value == self.Types.VARIABLE:
            return VariableParserToken(LexerToken.try_get_identifier_value(next(tokens)))
        if self.value == self.Types.VALUE:
            return ValueParserToken(LexerToken.try_get_identifier_value(next(tokens)))
        if self.value == self.Types.RETURN:
            return ReturnParserToken(LexerToken.try_get_return_value(next(tokens)))
        if self.value == self.Types.FUNCTION:
            token = next(tokens)
            if not isinstance(token, IdentLexerToken):
                raise RuntimeError(f"Expected IdentLexerToken, got {type(token)}")
            name = token.value
            paren_open = next(tokens)
            LexerToken.assert_type(paren_open, DelimLexerToken.Types.PAREN_OPEN)
            parameters = eat_until_discarding(tokens, DelimLexerToken.Types.PAREN_CLOSE)
            body = eat_until_discarding(tokens, KeywordLexerToken.Types.FUNCTION)
            return FunctionParserToken(name, parameters, body)
        if self.value == self.Types.LAMBDA:
            raise NotImplementedError("Lambdas not implemented yet")


class LiteralLexerToken(LexerToken):
    class Types(TokenTypeEnum):
        NUMBER = "NUMBER"
        COMMENT = "#"
        TRUE = "True"
        FALSE = "False"

    def __init__(self, token_type, word: Word):
        super().__init__(Word(token_type, word.debug_data))
        self.content = word.content

    def parse(self, tokens: Iterator["LexerToken"]):
        if self.value == self.Types.NUMBER:
            return NumberParserToken(int(self.content))
        if self.value in [self.Types.TRUE, self.Types.FALSE]:
            return BooleanParserToken(self.content)


class MacroLexerToken(LexerToken):
    class Types(TokenTypeEnum):
        PRINT = "__PRINT__"

    def parse(self, tokens: Iterator["LexerToken"]):
        return MacroParserToken(self.value.value)


class OpLexerToken(LexerToken):
    class Types(TokenTypeEnum):
        SUBTRACTION = "-"
        ADDITION = "+"
        EQUALITY = "=="
        GREATER = ">"
        LESSER = "<"
        GREATER_EQ = ">="
        LESSER_EQ = ">="
        ASSIGNMENT = "ASSIGN"
        RETRIEVAL = "RETRIEVE"

    def parse(self, tokens: Iterator["LexerToken"]):
        if self.value.value in ["-", "+"]:
            return ArithmeticOperatorParserToken(self.value.value)
        if self.value.value in ["==", ">", "<", ">=", "<="]:
            return BooleanOperatorParserToken(self.value.value)
        if self.value.value in ["ASSIGN", "RETRIEVE"]:
            targeted_variable = next(tokens)
            LexerToken.assert_instance_of(targeted_variable, IdentLexerToken)
            return DictionaryOperatorParserToken(self.value.value, targeted_variable.value)
