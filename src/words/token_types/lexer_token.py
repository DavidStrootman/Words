from abc import abstractmethod
from typing import Iterator, Type, Union

from words.exceptions.lexer_exceptions import UnexpectedTokenError, UnexpectedTokenTypeError, \
    IncorrectReturnCountError, InvalidTokenError, MissingTokenError, NoReturnTokenError
from words.helper.Debuggable import Debuggable
from words.helper.PrintableABC import PrintableABC
from words.helper.TokenTypeEnum import TokenTypeEnum
from words.lexer.lex_util import Word
from words.parser.parse_util import eat_until, eat_until_discarding
from words.token_types.parser_token import ParserToken, DictionaryOperatorParserToken, BooleanOperatorParserToken, \
    ArithmeticOperatorParserToken, BooleanParserToken, MacroParserToken, NumberParserToken, FunctionParserToken, \
    ReturnParserToken, ValueParserToken, VariableParserToken, IdentParserToken, IfParserToken, WhileParserToken, \
    CopyParserToken


class LexerToken(Debuggable, PrintableABC):
    """
    Abstract lexer token.
    """

    class Types(TokenTypeEnum):
        """Fallback for undefined token types."""
        UNDEFINED = "UNDEFINED"

    def __init__(self, word: Word):
        self.debug_data = word.debug_data
        self.value = self.Types(word.content)

    def debug_str(self) -> str:
        return f"\"{self.value}\" at line {self.debug_data}"

    @abstractmethod
    def parse(self, tokens: Iterator["LexerToken"]) -> ParserToken:
        """
        Parse the lexer token into a parser token.
        :param tokens: The list of lexer tokens, which might be used during parsing of this token depending on it's
        type.
        :return: A parser token
        """

    @staticmethod
    def assert_kind_of(token: "LexerToken", kind: Type["LexerToken"]) -> None:
        """
        Asserts that the provided token is of the provided kind. This method is used for recognizing syntax errors.

        :param token: The token to run the assertion on.
        :param kind: The asserted kind.
        :return: None
        """
        if not isinstance(token, kind):
            raise UnexpectedTokenError(token, kind)

    @staticmethod
    def assert_type(token: "LexerToken", type_: TokenTypeEnum) -> None:
        """
        Asserts that the provided token is of the provided type. This method is used for recognizing syntax errors.

        :param token: The token to run the assertion on.
        :param type_: The asserted type.
        :return: None
        """
        if token.value is not type_:
            raise UnexpectedTokenTypeError(token, type_)

    @staticmethod
    def try_get_return_value(token: "LexerToken") -> int:
        """
        Try to get a return value after a return statement.

        :param token: The literal (number) token that should provide the amount of return values
        :return: The amount of return values as an integer (1, 2 or 3).
        """
        LexerToken.assert_type(token, LiteralLexerToken.Types.NUMBER)
        if int(token.content) not in range(4):
            raise IncorrectReturnCountError(token)
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
        Delimiter lexer tokens cannot be parsed by themselves. They are parsed by the preceding function token.

        :param tokens: The list of lexer tokens, which might be used during parsing of this token depending on it's
         type.
        :return: None
        """
        raise InvalidTokenError(self)


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
        return IdentParserToken(self.debug_data, self.value)


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
        COPY = "COPY"
        VALUE = "VALUE"
        RETURN = "RETURN"
        FUNCTION = "|"
        LAMBDA = "λ"

    def debug_str(self) -> str:
        if self.value == self.Types.FUNCTION:
            return f"\"{self.value.value}\" at line {self.debug_data}"
        return super().debug_str()

    def parse(self, tokens: Iterator["LexerToken"]) -> Union[  # noqa: C901
        WhileParserToken, IfParserToken, VariableParserToken,
        ValueParserToken, ReturnParserToken, FunctionParserToken]:
        """
        Parse the lexer token into a parser token.
        :param tokens: The list of lexer tokens, which might be used during parsing of this token depending on its
        type.
        :return: A parser token
        """
        if self.value == self.Types.BEGIN:
            predicate = eat_until(tokens, [self.Types.WHILE])
            predicate_without_last_item = predicate[:-1]
            body = eat_until_discarding(tokens, [self.Types.REPEAT])
            if not body:
                raise MissingTokenError(self, "any token")
            return WhileParserToken(self.debug_data, predicate_without_last_item, body)

        if self.value == self.Types.WHILE:
            raise InvalidTokenError(self)

        if self.value == self.Types.REPEAT:
            raise InvalidTokenError(self)

        if self.value == self.Types.IF:
            try:
                if_body = eat_until(tokens, [self.Types.ELSE, self.Types.THEN])
            except StopIteration:
                raise MissingTokenError(self, self.Types.THEN.value)
            if if_body[-1].value == self.Types.ELSE:
                if_body = if_body[:-1]  # Discard ELSE token
                try:
                    else_body = eat_until_discarding(tokens, [self.Types.THEN])
                except StopIteration:
                    raise MissingTokenError(self, self.Types.THEN.value)
            else:
                if_body = if_body[:-1]  # Discard THEN token
                else_body = None
            return IfParserToken(self.debug_data, if_body, else_body)

        if self.value == self.Types.ELSE:
            raise InvalidTokenError(self)

        if self.value == self.Types.THEN:
            raise InvalidTokenError(self)

        if self.value == self.Types.VARIABLE:
            try:
                token = next(tokens)
            except StopIteration:
                raise MissingTokenError(self, IdentLexerToken)

            LexerToken.assert_kind_of(token, IdentLexerToken)
            return VariableParserToken(self.debug_data, token.value)

        if self.value == self.Types.VALUE:
            try:
                token = next(tokens)
            except StopIteration:
                raise MissingTokenError(self, IdentLexerToken)

            LexerToken.assert_kind_of(token, IdentLexerToken)

            return ValueParserToken(self.debug_data, token.value)

        if self.value == self.Types.RETURN:
            try:
                return_value = LexerToken.try_get_return_value(next(tokens))
            except StopIteration:
                raise MissingTokenError(self, LiteralLexerToken.Types.NUMBER.value)
            return ReturnParserToken(self.debug_data, return_value)

        if self.value == self.Types.FUNCTION:
            token = next(tokens)

            if not isinstance(token, IdentLexerToken):
                raise UnexpectedTokenError(token, IdentLexerToken)

            function_name = token.value

            paren_open = next(tokens)
            LexerToken.assert_type(paren_open, DelimLexerToken.Types.PAREN_OPEN)

            try:
                parameters = eat_until_discarding(tokens, [DelimLexerToken.Types.PAREN_CLOSE])
            except StopIteration:
                raise MissingTokenError(self, DelimLexerToken.Types.PAREN_CLOSE.value)

            try:
                body = eat_until_discarding(tokens, [KeywordLexerToken.Types.FUNCTION])
                if not any(isinstance(token, ReturnParserToken) for token in body):
                    raise NoReturnTokenError(self)
            except StopIteration:
                raise MissingTokenError(self, f"closing \"{KeywordLexerToken.Types.FUNCTION.value}\"")

            if not all(isinstance(token, ValueParserToken) for token in parameters):
                raise RuntimeError(
                    f"Got token that is not a ValueParserToken in Function Parameters in function {function_name}")
            return FunctionParserToken(self.debug_data, function_name, parameters, body)

        if self.value == self.Types.COPY:
            return CopyParserToken(self.debug_data)

        if self.value == self.Types.LAMBDA:
            raise NotImplementedError("Lambdas not implemented yet.")

        raise NotImplementedError(f"Keyword token with value {self.value} not implemented.")


class LiteralLexerToken(LexerToken):
    """
    A literal token holds a literal value that does not get changed during lexing or parsing.
    """

    class Types(TokenTypeEnum):
        NUMBER = "NUMBER"
        COMMENT = "#"
        TRUE = "True"
        FALSE = "False"

    def __init__(self, token_type: str, word: Word):
        super().__init__(Word(token_type, word.debug_data))
        self.content = word.content

    def debug_str(self) -> str:
        if self.value is self.Types.COMMENT:
            return f"\"COMMENT\" at line {self.debug_data}"
        if self.value is self.Types.NUMBER:
            return f"{int(self.content):,}"
        return super().debug_str()

    def parse(self, tokens: Iterator["LexerToken"]) -> Union[NumberParserToken, BooleanParserToken]:
        """
        Parse the lexer token into a parser token.
        :param tokens: The list of lexer tokens, which might be used during parsing of this token depending on it's
        type.
        :return: Either a number parser token or a boolean parser token based on the type of lexer token.
        """
        if self.value == self.Types.COMMENT:
            raise InvalidTokenError(self)
        if self.value == self.Types.NUMBER:
            number = int(self.content)
            if number > 0xFFFFFFFF:
                raise ValueError(f"Number is too big, must be at most a 32 bit unsigned integer(4,294,967,295), got "
                                 f"{self.debug_str()}.")

            return NumberParserToken(self.debug_data, number)
        if self.value in [self.Types.TRUE, self.Types.FALSE]:
            return BooleanParserToken(self.debug_data, self.content)


class MacroLexerToken(LexerToken):
    class Types(TokenTypeEnum):
        PRINT = "__PRINT__"

    def parse(self, tokens: Iterator["LexerToken"]):
        """
        Parse the lexer token into a parser token.
        :param tokens: The list of lexer tokens, which might be used during parsing of this token depending on its
        type.
        :return: A Macro parser token.
        """
        return MacroParserToken(self.debug_data, self.value.value)


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
        LESSER_EQ = "<="
        ASSIGNMENT = "ASSIGN"

    def parse(self, tokens: Iterator["LexerToken"]) -> Union[
        ArithmeticOperatorParserToken, BooleanOperatorParserToken, DictionaryOperatorParserToken]:
        """
        Parse the lexer token into a parser token.
        :param tokens: The list of lexer tokens, which might be used during parsing of this token depending on it's
        type.
        :return: One of the three operator parser token types:
        ArithmeticOperatorParserToken, BooleanOperatorParserToken or DictionaryOperatorParserToken,
        based on the type of lexer token.
        """
        if self.value.value in ["-", "+"]:
            return ArithmeticOperatorParserToken(self.debug_data, self.value.value)
        if self.value.value in ["==", ">", "<", ">=", "<="]:
            return BooleanOperatorParserToken(self.debug_data, self.value.value)
        if self.value.value in ["ASSIGN"]:
            try:
                targeted_variable = next(tokens)
            except StopIteration:
                raise MissingTokenError(self, IdentLexerToken)

            LexerToken.assert_kind_of(targeted_variable, IdentLexerToken)
            return DictionaryOperatorParserToken(self.debug_data, self.value.value, targeted_variable.value)
