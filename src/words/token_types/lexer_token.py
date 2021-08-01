from abc import ABC, abstractmethod
from typing import Iterator, Type, Union

from words.helper.token_type_enum import TokenTypeEnum
from words.lexer.lex_util import Word
from words.parser.parse_util import eat_until, eat_until_discarding
from words.token_types.parser_token import ParserToken, DictionaryOperatorParserToken, BooleanOperatorParserToken, \
    ArithmeticOperatorParserToken, BooleanParserToken, MacroParserToken, NumberParserToken, FunctionParserToken, \
    ReturnParserToken, ValueParserToken, VariableParserToken, IdentParserToken, IfParserToken, WhileParserToken


class PrintableABC(type(ABC)):
    def __str__(self):
        return f"{self.__name__}"


class LexerToken(metaclass=PrintableABC):
    """
    Abstract lexer token.
    """

    class Types(TokenTypeEnum):
        """Fallback for undefined token types."""
        UNDEFINED = "UNDEFINED"

    def __init__(self, word: Word):
        self.debug_data = word.debug_data
        self.value = self.Types(word.content)

    def debug_str(self):
        return f"\"{self.value}\" at line {self.debug_data}"

    @abstractmethod
    def parse(self, tokens: Iterator["LexerToken"]) -> ParserToken:
        """
        Parse the lexer token into a parser token.
        :param tokens: The list of lexer tokens, which might be used during parsing of this token depending on it's
        type.
        :return: A parser token
        """
        pass

    @staticmethod
    def assert_kind_of(token: "LexerToken", kind: Type["LexerToken"]) -> None:
        """
        Asserts that the provided token is of the provided kind. This method is used for recognizing syntax errors.

        :param token: The token to run the assertion on.
        :param kind: The asserted kind.
        :return: None
        """
        if not isinstance(token, kind):
            raise SyntaxError(f"Expected {kind}, got {type(token)} with value {token.debug_str()}")

    @staticmethod
    def assert_type(token: "LexerToken", type_: TokenTypeEnum) -> None:
        """
        Asserts that the provided token is of the provided type. This method is used for recognizing syntax errors.

        :param token: The token to run the assertion on.
        :param type_: The asserted type.
        :return: None
        """
        if token.value is not type_:
            raise SyntaxError(f"Expected {type_}, got {type(token)} with value {token.debug_str()}.")

    @staticmethod
    def try_get_identifier_value(token: "LexerToken") -> str:
        # TODO: Refactor this into assert_kind_of
        if not isinstance(token, IdentLexerToken):
            raise SyntaxError(f"Expected variable name, got {type(token)} with value {token.debug_str()}.")
        return token.value

    @staticmethod
    def try_get_return_value(token: "LexerToken") -> int:
        """
        Try to get a return value after a return statement.

        :param token: The literal (number) token that should provide the amount of return values
        :return: The amount of return values as an integer (1, 2 or 3).
        """
        LexerToken.assert_kind_of(token, LiteralLexerToken)
        if int(token.content) not in range(3):
            raise SyntaxError(f"Got too many return values: {token.debug_str()}, expected 0, 1 or 2")
        return int(token.content)


class DelimLexerToken(LexerToken):
    """
    A delimiter token is used to start and end a series of values.
    """

    class Types(TokenTypeEnum):
        PAREN_OPEN = "("
        PAREN_CLOSE = ")"

    def parse(self, tokens: Iterator["LexerToken"]) -> None:
        """
        Parse the lexer token into a parser token.
        :param tokens: The list of lexer tokens, which might be used during parsing of this token depending on it's
        type.
        :return: None
        """
        raise NotImplementedError(f"Tried to parse a delimiter token: {self.debug_str()}, this should be handled by its parent.")


class IdentLexerToken(LexerToken):
    """
    An identifier token holds the name of a variable or function.
    """

    def __init__(self, word: Word):
        super().__init__(Word("UNDEFINED", word.debug_data))
        self.value = word.content

    def parse(self, tokens: Iterator["LexerToken"]) -> IdentParserToken:
        """
        Parse the lexer token into a parser token.
        :param tokens: The list of lexer tokens, which might be used during parsing of this token depending on it's
        type.
        :return: Identifier parser token.
        """
        return IdentParserToken(self.value)


class KeywordLexerToken(LexerToken):
    """
    A keyword token holds builtin words that mean something in the language. These keywords cannot be used as
    variable names.
    """

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

    def _unexpected_token_error(self) -> SyntaxError:
        return SyntaxError(f"Found unexpected {self.debug_str()}.")

    def parse(self, tokens: Iterator["LexerToken"]) -> Union[
        WhileParserToken, IfParserToken, VariableParserToken, ValueParserToken, ReturnParserToken, FunctionParserToken]:
        """
        Parse the lexer token into a parser token.
        :param tokens: The list of lexer tokens, which might be used during parsing of this token depending on it's
        type.
        :return: A parser token
        """
        if self.value == self.Types.BEGIN:
            predicate = eat_until(tokens, [self.Types.WHILE])
            predicate_without_last_item = predicate[:-1]
            statements = eat_until_discarding(tokens, [self.Types.REPEAT])
            return WhileParserToken(predicate_without_last_item, statements)
        if self.value == self.Types.WHILE:
            raise self._unexpected_token_error()
        if self.value == self.Types.REPEAT:
            raise self._unexpected_token_error()
        if self.value == self.Types.IF:
            if_body = eat_until(tokens, [self.Types.ELSE, self.Types.THEN])
            if if_body[-1].value == self.Types.ELSE:
                if_body = if_body[:-1]  # Discard ELSE token
                else_body = eat_until_discarding(tokens, [self.Types.THEN])
            else:
                if_body = if_body[:-1]  # Discard THEN token
                else_body = None
            return IfParserToken(if_body, else_body)
        if self.value == self.Types.ELSE:
            raise self._unexpected_token_error()
        if self.value == self.Types.THEN:
            raise self._unexpected_token_error()
        if self.value == self.Types.VARIABLE:
            return VariableParserToken(LexerToken.try_get_identifier_value(next(tokens)))
        if self.value == self.Types.VALUE:
            return ValueParserToken(LexerToken.try_get_identifier_value(next(tokens)))
        if self.value == self.Types.RETURN:
            return ReturnParserToken(LexerToken.try_get_return_value(next(tokens)))
        if self.value == self.Types.FUNCTION:
            token = next(tokens)
            if not isinstance(token, IdentLexerToken):
                raise SyntaxError(f"Expected identifier, got {type(token)} with value {token.debug_str()}.")
            name = token.value
            paren_open = next(tokens)
            LexerToken.assert_type(paren_open, DelimLexerToken.Types.PAREN_OPEN)
            parameters = eat_until_discarding(tokens, [DelimLexerToken.Types.PAREN_CLOSE])
            body = eat_until_discarding(tokens, [KeywordLexerToken.Types.FUNCTION])
            return FunctionParserToken(name, parameters, body)
        if self.value == self.Types.LAMBDA:
            raise NotImplementedError("Lambdas not implemented yet")


class LiteralLexerToken(LexerToken):
    """
    A literal token holds a literal value that does not get changed during lexing or parsing.
    """

    class Types(TokenTypeEnum):
        NUMBER = "NUMBER"
        COMMENT = "#"
        TRUE = "True"
        FALSE = "False"

    def __init__(self, token_type, word: Word):
        super().__init__(Word(token_type, word.debug_data))
        self.content = word.content

    def parse(self, tokens: Iterator["LexerToken"]) -> Union[NumberParserToken, BooleanParserToken]:
        """
        Parse the lexer token into a parser token.
        :param tokens: The list of lexer tokens, which might be used during parsing of this token depending on it's
        type.
        :return: Either a number parser token or a boolean parser token based on the type of lexer token.
        """
        if self.value == self.Types.NUMBER:
            return NumberParserToken(int(self.content))
        if self.value in [self.Types.TRUE, self.Types.FALSE]:
            return BooleanParserToken(self.content)


class MacroLexerToken(LexerToken):
    class Types(TokenTypeEnum):
        PRINT = "__PRINT__"

    def parse(self, tokens: Iterator["LexerToken"]):
        """
        Parse the lexer token into a parser token.
        :param tokens: The list of lexer tokens, which might be used during parsing of this token depending on it's
        type.
        :return: A Macro parser token.
        """
        return MacroParserToken(self.value.value)


class OpLexerToken(LexerToken):
    """
    An operator token holds a Keyword that is used as an operator on literals or identifiers
    """

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

    def parse(self, tokens: Iterator["LexerToken"]) -> Union[
        ArithmeticOperatorParserToken, BooleanOperatorParserToken, DictionaryOperatorParserToken]:
        """
        Parse the lexer token into a parser token.
        :param tokens: The list of lexer tokens, which might be used during parsing of this token depending on it's
        type.
        :return: One of the three operator parser token types: ArithmeticOperatorParserToken, BooleanOperatorParserToken
        or DictionaryOperatorParserToken, based on the type of lexer token.
        """
        if self.value.value in ["-", "+"]:
            return ArithmeticOperatorParserToken(self.value.value)
        if self.value.value in ["==", ">", "<", ">=", "<="]:
            return BooleanOperatorParserToken(self.value.value)
        if self.value.value in ["ASSIGN", "RETRIEVE"]:
            targeted_variable = next(tokens)
            LexerToken.assert_kind_of(targeted_variable, IdentLexerToken)
            return DictionaryOperatorParserToken(self.value.value, targeted_variable.value)
