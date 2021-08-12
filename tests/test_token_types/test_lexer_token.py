from typing import Iterator, Type
import pytest
from words.lexer.lex_util import Word, DebugData
from words.exceptions.lexer_exceptions import InvalidTokenError, MissingTokenError, UnexpectedTokenError
from words.token_types.lexer_token import LexerToken, DelimLexerToken, IdentLexerToken, LiteralLexerToken, \
    KeywordLexerToken
from words.token_types.parser_token import ParserToken, IdentParserToken, WhileParserToken, IfParserToken, \
    VariableParserToken, ValueParserToken


class TestLexerToken:
    def test_undefined_type(self):
        class ConcreteLexerToken(LexerToken):
            def parse(self, tokens: Iterator[LexerToken]):
                pass

        with pytest.raises(ValueError):
            ConcreteLexerToken(Word("test", DebugData(0)))
        ConcreteLexerToken(Word("UNDEFINED", DebugData(1)))


def _assert_token_parse_returns(token: LexerToken,
                                tokens: Iterator[LexerToken],
                                expected_output: Type[ParserToken]):
    actual_output = token.parse(tokens)
    assert isinstance(actual_output, expected_output)


def _assert_token_parse_raises(token: LexerToken,
                               tokens: Iterator[LexerToken],
                               raises: Type[Exception]):
    with pytest.raises(raises):
        token.parse(tokens)


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
