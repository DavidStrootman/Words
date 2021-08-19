from typing import Iterator, Type
import pytest
from words.lexer.lex_util import Word, DebugData
from words.exceptions.lexer_exceptions import InvalidTokenError, MissingTokenError, UnexpectedTokenError, \
    UnexpectedTokenTypeError, IncorrectReturnCountError
from words.token_types.lexer_token import LexerToken, DelimLexerToken, IdentLexerToken, LiteralLexerToken, \
    KeywordLexerToken, MacroLexerToken, OpLexerToken
from words.token_types.parser_token import ParserToken, IdentParserToken, WhileParserToken, IfParserToken, \
    VariableParserToken, ValueParserToken, ReturnParserToken, FunctionParserToken, LambdaParserToken, \
    NumberParserToken, BooleanParserToken, MacroParserToken, ArithmeticOperatorParserToken, \
    BooleanOperatorParserToken, DictionaryOperatorParserToken


def _assert_token_parse_returns(token: LexerToken,
                                tokens: Iterator[LexerToken],
                                expected_output: Type[ParserToken]):
    actual_output = token.parse(tokens)
    assert isinstance(actual_output, expected_output)


def _assert_token_parse_raises(token: LexerToken,
                               tokens: Iterator[LexerToken],
                               raises: Type[Exception], capsys=None):
    with pytest.raises(raises):
        token.parse(tokens)
        if capsys:
            print(capsys.readouterr())


class TestLexerToken:
    def test_undefined_type(self):
        class ConcreteLexerToken(LexerToken):
            """Concrete implementation of abstract lexer token."""

            def parse(self, tokens: Iterator[LexerToken]):
                """Concrete implementation of parse method."""

        with pytest.raises(ValueError):
            ConcreteLexerToken(Word("test", DebugData(0)))
        ConcreteLexerToken(Word("UNDEFINED", DebugData(1)))

    def test_assert_kind_of_positive(self):
        LexerToken.assert_kind_of(LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("0", DebugData(0))),
                                  LiteralLexerToken)

    def test_assert_kind_of_negative(self):
        with pytest.raises(UnexpectedTokenError):
            LexerToken.assert_kind_of(LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("0", DebugData(0))),
                                      IdentLexerToken)

    def test_assert_type_positive(self):
        LexerToken.assert_type(LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("0", DebugData(0))),
                               LiteralLexerToken.Types.NUMBER)

    def test_assert_type_negative(self):
        with pytest.raises(UnexpectedTokenTypeError):
            LexerToken.assert_type(LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("0", DebugData(0))),
                                   LiteralLexerToken.Types.TRUE)

    def test_try_get_return_value_positive(self):
        token = LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("1", DebugData(0)))
        assert isinstance(LexerToken.try_get_return_value(token), int)

    def test_try_get_return_value_invalid_type(self):
        token = LiteralLexerToken(LiteralLexerToken.Types.TRUE.value, Word("True", DebugData(0)))
        with pytest.raises(UnexpectedTokenTypeError):
            LexerToken.try_get_return_value(token)

    def test_try_get_return_value_invalid_return_count_high(self):
        token = LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("4", DebugData(0)))
        with pytest.raises(IncorrectReturnCountError):
            LexerToken.try_get_return_value(token)

    def test_try_get_return_value_invalid_return_count_low(self):
        token = LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("-1", DebugData(0)))
        with pytest.raises(IncorrectReturnCountError):
            LexerToken.try_get_return_value(token)


class TestDelimLexerToken:
    def test_parse(self):
        """Delimiter tokens cannot be parsed."""
        _assert_token_parse_raises(DelimLexerToken(Word("(", DebugData(0))), iter([]), InvalidTokenError)


class TestIdentLexerToken:
    def test_parse(self):
        """Identifiers are not enriched during parsing and simply return the parser version of the same token."""
        _assert_token_parse_returns(IdentLexerToken(Word("IDENT_NAME", DebugData(0))), iter([]), IdentParserToken)


class TestKeywordLexerToken:
    def test_parse_while_statement_positive(self):
        # Parsing a while statement, starting with a BEGIN keyword
        while_statement = iter([
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("1", DebugData(0))),
            KeywordLexerToken(Word(KeywordLexerToken.Types.WHILE.value, DebugData(0))),
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("1", DebugData(0))),
            KeywordLexerToken(Word(KeywordLexerToken.Types.REPEAT.value, DebugData(0))),
        ])
        _assert_token_parse_returns(KeywordLexerToken(Word("BEGIN", DebugData(0))), while_statement, WhileParserToken)

    def test_parse_out_of_place_while_statement_tokens(self):
        """Parts of a while statement cannot be parsed on their own, and must be parsed by preceding tokens."""
        # Parsing an out of place WHILE token
        _assert_token_parse_raises(KeywordLexerToken(Word("WHILE", DebugData(0))), iter([]), InvalidTokenError)

        # Parsing an out of place REPEAT token
        _assert_token_parse_raises(KeywordLexerToken(Word("REPEAT", DebugData(0))), iter([]), InvalidTokenError)

    def test_parse_if_statement_positive(self):
        # Parsing a complete correct IF statement
        if_statement_positive = iter([
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("0", DebugData(0))),
            KeywordLexerToken(Word(KeywordLexerToken.Types.THEN.value, DebugData(0))),
        ])
        _assert_token_parse_returns(KeywordLexerToken(Word("IF", DebugData(0))), if_statement_positive, IfParserToken)

    def test_parse_if_statement_with_else_positive(self):
        """Parsing a complete correct IF statement with an ELSE."""
        if_statement_with_else_positive = iter([
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("0", DebugData(0))),
            KeywordLexerToken(Word(KeywordLexerToken.Types.ELSE.value, DebugData(0))),
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("0", DebugData(0))),
            KeywordLexerToken(Word(KeywordLexerToken.Types.THEN.value, DebugData(0))),
        ])
        _assert_token_parse_returns(KeywordLexerToken(Word("IF", DebugData(0))), if_statement_with_else_positive,
                                    IfParserToken)

    def test_parse_if_statement_negative(self):
        """Parsing an invalid IF statement without a THEN."""
        if_statement_negative = iter([
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("0", DebugData(0)))
        ])
        _assert_token_parse_raises(KeywordLexerToken(Word("IF", DebugData(0))), if_statement_negative,
                                   MissingTokenError)

    def test_parse_if_statement_with_else_negative(self):
        """Parsing an invalid IF statement with an ELSE, but without a THEN."""
        if_statement_with_else_negative = iter([
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("0", DebugData(0))),
            KeywordLexerToken(Word(KeywordLexerToken.Types.ELSE.value, DebugData(0))),
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("0", DebugData(0)))
        ])
        _assert_token_parse_raises(KeywordLexerToken(Word("IF", DebugData(0))), if_statement_with_else_negative,
                                   MissingTokenError)

    def test_parse_if_statement_no_body(self):
        """Parsing an IF statement without a body, which is valid."""
        if_statement_without_body = iter([
            KeywordLexerToken(Word(KeywordLexerToken.Types.ELSE.value, DebugData(0))),
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("0", DebugData(0))),
            KeywordLexerToken(Word(KeywordLexerToken.Types.THEN.value, DebugData(0))),
        ])
        _assert_token_parse_returns(KeywordLexerToken(Word("IF", DebugData(0))), if_statement_without_body,
                                    IfParserToken)

    def test_parse_if_statement_no_more_tokens(self):
        """An IF statement cannot be the last token in a file."""
        _assert_token_parse_raises(KeywordLexerToken(Word("IF", DebugData(0))), iter([]), MissingTokenError)

    def test_parse_out_of_place_if_statement_tokens(self):
        """Parts of an if statement cannot be parsed on their own, and must be parsed by preceding tokens."""
        # Parsing an out of place ELSE token
        _assert_token_parse_raises(KeywordLexerToken(Word("ELSE", DebugData(0))), iter([]), InvalidTokenError)

        # Parsing an out of place THEN token
        _assert_token_parse_raises(KeywordLexerToken(Word("THEN", DebugData(0))), iter([]), InvalidTokenError)

    def test_parse_variable_token_positive(self):
        """Parse a variable token with a variable name."""
        variable_token_positive = iter([
            IdentLexerToken(Word("VARIABLE_NAME", DebugData(0)))
        ])
        _assert_token_parse_returns(KeywordLexerToken(Word("VARIABLE", DebugData(0))), variable_token_positive,
                                    VariableParserToken)

    def test_parse_variable_token_no_identifier(self):
        """Parse a VARIABLE token without following it with an identifier to use as the variable name."""
        variable_token_no_identifier = iter([
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("0", DebugData(0)))
        ])
        _assert_token_parse_raises(KeywordLexerToken(Word("VARIABLE", DebugData(0))), variable_token_no_identifier,
                                   UnexpectedTokenError)

    def test_parse_variable_token_no_more_tokens(self):
        """A VARIABLE token cannot be the last token in a file."""
        _assert_token_parse_raises(KeywordLexerToken(Word("VARIABLE", DebugData(0))), iter([]), MissingTokenError)

    def test_parse_value_token_positive(self):
        """Parse a VALUE token with a value name."""
        value_token_positive = iter([
            IdentLexerToken(Word("VALUE_NAME", DebugData(0)))
        ])
        _assert_token_parse_returns(KeywordLexerToken(Word("VALUE", DebugData(0))), value_token_positive,
                                    ValueParserToken)

    def test_parse_value_token_no_identifier(self):
        """Parse a VALUE token without following it with an identifier to use as the value name."""
        value_token_no_identifier = iter([
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("0", DebugData(0)))
        ])
        _assert_token_parse_raises(KeywordLexerToken(Word("VALUE", DebugData(0))), value_token_no_identifier,
                                   UnexpectedTokenError)

    def test_parse_value_token_no_more_tokens(self):
        """A VALUE token cannot be the last token in a file."""
        _assert_token_parse_raises(KeywordLexerToken(Word("VALUE", DebugData(0))), iter([]), MissingTokenError)

    def test_parse_return_statement_positive(self):
        """Parse a RETURN statement with a return count."""
        return_statement_positive = iter([
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("0", DebugData(0)))
        ])
        _assert_token_parse_returns(KeywordLexerToken(Word("RETURN", DebugData(0))), return_statement_positive,
                                    ReturnParserToken)

    def test_parse_return_token_no_value(self):
        """A RETURN token must be provided a return count."""
        return_statement_no_value = iter([
            IdentLexerToken(Word("INCORRECT_IDENT", DebugData(0)))
        ])
        _assert_token_parse_raises(KeywordLexerToken(Word("RETURN", DebugData(0))), return_statement_no_value,
                                   UnexpectedTokenTypeError)

    def test_parse_return_token_no_more_tokens(self):
        """A RETURN token cannot be the last token in a file."""
        _assert_token_parse_raises(KeywordLexerToken(Word("RETURN", DebugData(0))), iter([]), MissingTokenError)

    def test_parse_function_token_positive(self):
        """Parse a FUNCTION with a parameter, a correct body and a return."""
        function_token_positive = iter([
            IdentLexerToken(Word("FUNCTION_NAME", DebugData(0))),
            DelimLexerToken(Word("(", DebugData(0))),
            KeywordLexerToken(Word("VALUE", DebugData(0))),
            IdentLexerToken(Word("VALUE_NAME", DebugData(0))),
            DelimLexerToken(Word(")", DebugData(0))),
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("9", DebugData(0))),
            KeywordLexerToken(Word("RETURN", DebugData(0))),
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("1", DebugData(0))),
            KeywordLexerToken(Word("|", DebugData(0)))
        ])
        _assert_token_parse_returns(KeywordLexerToken(Word("|", DebugData(0))), function_token_positive,
                                    FunctionParserToken)

    def test_parse_function_token_no_name(self):
        """A FUNCTION token must be followed by an identifier token as its name."""
        function_token_no_name = iter([
            DelimLexerToken(Word("(", DebugData(0))),
            KeywordLexerToken(Word("VALUE", DebugData(0))),
            IdentLexerToken(Word("VALUE_NAME", DebugData(0))),
            DelimLexerToken(Word(")", DebugData(0))),
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("9", DebugData(0))),
        ])
        _assert_token_parse_raises(KeywordLexerToken(Word("|", DebugData(0))), function_token_no_name,
                                   UnexpectedTokenError)

    def test_parse_function_token_no_closing_token(self):
        """A FUNCTION token must be closed with another function token"""
        function_token_no_return = iter([
            IdentLexerToken(Word("FUNCTION_NAME", DebugData(0))),
            DelimLexerToken(Word("(", DebugData(0))),
            KeywordLexerToken(Word("VALUE", DebugData(0))),
            IdentLexerToken(Word("VALUE_NAME", DebugData(0))),
            DelimLexerToken(Word(")", DebugData(0))),
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("9", DebugData(0))),
        ])
        _assert_token_parse_raises(KeywordLexerToken(Word("|", DebugData(0))), function_token_no_return,
                                   MissingTokenError)

    def test_parse_function_token_missing_params(self):
        """A FUNCTION TOKEN must contain open and closing brackets for parameters."""
        function_token_missing_params = iter([
            IdentLexerToken(Word("FUNCTION_NAME", DebugData(0))),
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("1", DebugData(0))),
            KeywordLexerToken(Word("|", DebugData(0)))
        ])
        _assert_token_parse_raises(KeywordLexerToken(Word("|", DebugData(0))), function_token_missing_params,
                                   UnexpectedTokenTypeError)

    def test_parse_function_token_no_params(self):
        """A FUNCTION token should support having no parameters."""
        function_token_no_return = iter([
            IdentLexerToken(Word("FUNCTION_NAME", DebugData(0))),
            DelimLexerToken(Word("(", DebugData(0))),
            DelimLexerToken(Word(")", DebugData(0))),
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("9", DebugData(0))),
            KeywordLexerToken(Word("RETURN", DebugData(0))),
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("0", DebugData(0))),
            KeywordLexerToken(Word("|", DebugData(0)))
        ])
        _assert_token_parse_returns(KeywordLexerToken(Word("|", DebugData(0))), function_token_no_return,
                                    FunctionParserToken)

    def test_parse_function_token_no_body(self):
        """A FUNCTION token should support having only a return token."""
        function_token_no_body = iter([
            IdentLexerToken(Word("FUNCTION_NAME", DebugData(0))),
            DelimLexerToken(Word("(", DebugData(0))),
            KeywordLexerToken(Word("VALUE", DebugData(0))),
            IdentLexerToken(Word("VALUE_NAME", DebugData(0))),
            DelimLexerToken(Word(")", DebugData(0))),
            KeywordLexerToken(Word("RETURN", DebugData(0))),
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("0", DebugData(0))),
            KeywordLexerToken(Word("|", DebugData(0)))
        ])
        _assert_token_parse_returns(KeywordLexerToken(Word("|", DebugData(0))), function_token_no_body,
                                    FunctionParserToken)

    def test_parse_function_token_no_closing_bracket(self):
        """
        Since parsing the brackets for parameters is handled by the function,
        it is responsible for this happening correctly.
        """
        function_token_no_closing_bracket = iter([
            IdentLexerToken(Word("FUNCTION_NAME", DebugData(0))),
            DelimLexerToken(Word("(", DebugData(0))),
            KeywordLexerToken(Word("VALUE", DebugData(0))),
            IdentLexerToken(Word("VALUE_NAME", DebugData(0))),
        ])
        _assert_token_parse_raises(KeywordLexerToken(Word("|", DebugData(0))), function_token_no_closing_bracket,
                                   MissingTokenError)

    @pytest.mark.xfail(reason="Lambdas are not implemented.")
    def test_parse_lambda_token_positive(self):
        """Parse a LAMBDA with a parameter, a correct body and a return."""
        lambda_token_positive = iter([
            DelimLexerToken(Word("(", DebugData(0))),
            KeywordLexerToken(Word("VALUE", DebugData(0))),
            IdentLexerToken(Word("VALUE_NAME", DebugData(0))),
            DelimLexerToken(Word(")", DebugData(0))),
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("9", DebugData(0))),
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("1", DebugData(0))),
            KeywordLexerToken(Word("λ", DebugData(0)))
        ])
        _assert_token_parse_returns(KeywordLexerToken(Word("λ", DebugData(0))), lambda_token_positive,
                                    LambdaParserToken)


class TestLiteralLexerToken:
    def test_parse_number_token_positive(self):
        """Parse a number literal."""
        _assert_token_parse_returns(LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("10", DebugData(0))),
                                    iter([]), NumberParserToken)

    def test_parse_number_token_incorrect_type(self):
        """Parse a number with a character as value."""
        _assert_token_parse_raises(LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("a", DebugData(0))),
                                   iter([]), ValueError)

    def test_parse_number_token_too_large(self, capsys):
        """Numbers must fit into a 32 bit register for correct compilation."""
        _assert_token_parse_raises(
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word(str(0x1000000000), DebugData(0))),
            iter([]), ValueError, capsys)

    def test_parse_boolean_token_positive(self):
        """Parse a boolean literal."""
        _assert_token_parse_returns(LiteralLexerToken(LiteralLexerToken.Types.TRUE.value, Word("True", DebugData(0))),
                                    iter([]), BooleanParserToken)
        _assert_token_parse_returns(LiteralLexerToken(LiteralLexerToken.Types.FALSE.value, Word("True", DebugData(0))),
                                    iter([]), BooleanParserToken)

    def test_parsing_comment_token(self):
        """Comments cannot be parsed, since they are removed during lexing."""
        _assert_token_parse_raises(LiteralLexerToken(LiteralLexerToken.Types.COMMENT.value, Word("#", DebugData(0))),
                                   iter([]), InvalidTokenError)


class TestMacroLexerToken:
    def test_parse_macro_token(self):
        """Macros are not enriched during parsing and simply return the parser version of the same token."""
        _assert_token_parse_returns(MacroLexerToken(Word("__PRINT__", DebugData(0))), iter([]), MacroParserToken)


class TestOpLexerToken:
    def test_parse_subtraction_op_token(self):
        _assert_token_parse_returns(OpLexerToken(Word("-", DebugData(0))), iter([]), ArithmeticOperatorParserToken)

    def test_parse_addition_op_token(self):
        _assert_token_parse_returns(OpLexerToken(Word("+", DebugData(0))), iter([]), ArithmeticOperatorParserToken)

    def test_parse_equality_op_token(self):
        _assert_token_parse_returns(OpLexerToken(Word("==", DebugData(0))), iter([]), BooleanOperatorParserToken)

    def test_parse_greater_op_token(self):
        _assert_token_parse_returns(OpLexerToken(Word(">", DebugData(0))), iter([]), BooleanOperatorParserToken)

    def test_parse_lesser_op_token(self):
        _assert_token_parse_returns(OpLexerToken(Word("<", DebugData(0))), iter([]), BooleanOperatorParserToken)

    def test_parse_greater_eq_op_token(self):
        _assert_token_parse_returns(OpLexerToken(Word(">=", DebugData(0))), iter([]), BooleanOperatorParserToken)

    def test_parse_lesser_eq_op_token(self):
        _assert_token_parse_returns(OpLexerToken(Word("<=", DebugData(0))), iter([]), BooleanOperatorParserToken)

    def test_parse_assignment_op_token_positive(self):
        ident = IdentLexerToken(Word("SOME_VARIABLE", DebugData(0)))
        _assert_token_parse_returns(OpLexerToken(Word("ASSIGN", DebugData(0))), iter([ident]),
                                    DictionaryOperatorParserToken)

    def test_parse_dictionary_operator_token_no_more_tokens(self):
        """Dictionary operator tokens are always followed by an identifier as their name or value."""
        _assert_token_parse_raises(OpLexerToken(Word("ASSIGN", DebugData(0))), iter([]), MissingTokenError)
