from words.token_types.lexer_token import *
from words.token_types.parser_token import *
import pytest


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
        """Delimiter tokens cannot be parsed"""
        _assert_token_parse_raises(DelimLexerToken(Word("(", DebugData(0))), iter([]), InvalidTokenError)


class TestIdentLexerToken:
    def test_parse(self):
        """Identifiers are not enriched during parsing and simply return the parser version of the same token."""
        _assert_token_parse_returns(IdentLexerToken(Word("IDENT_NAME", DebugData(0))), iter([]), IdentParserToken)


class TestKeywordLexerToken:
    def test_parse(self):
        # Parsing a while statement, starting with a BEGIN keyword.
        while_statement = iter([
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("1", DebugData(0))),
            KeywordLexerToken(Word(KeywordLexerToken.Types.WHILE.value, DebugData(0))),
            LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, Word("1", DebugData(0))),
            KeywordLexerToken(Word(KeywordLexerToken.Types.REPEAT.value, DebugData(0))),
        ])
        _assert_token_parse_returns(KeywordLexerToken(Word("BEGIN", DebugData(0))), while_statement, WhileParserToken)
        # Parsing a while token.
        _assert_token_parse_raises(KeywordLexerToken(Word("WHILE", DebugData(0))), iter([]), InvalidTokenError)
