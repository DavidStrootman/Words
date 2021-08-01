import pytest
from typing import Iterator, Type
from words.lexer.lex_util import DebugData, Word
from words.lexer.lex import Lexer
from words.token_types.lexer_token import *
from pathlib import Path
from os import remove as remove_file


class TestLexer:
    @staticmethod
    def _lex_from_file(file_name: str, content: str, open_mode="w") -> Iterator[LexerToken]:
        """Create a .word file and lex tokens from the file."""
        with open(file_name, open_mode) as file:
            file.write(content)
        lexer = Lexer()
        tokens = lexer.lex_file(Path(f"./{file_name}"))
        remove_file(file_name)
        return tokens

    def test_lex_file(self):
        """Lex one token from a file."""
        file_name = "test_lex_file.word"
        content = "2"
        tokens = self._lex_from_file(file_name, content)
        first_token = next(tokens)

        # Assert token is read correctly from file.
        assert isinstance(first_token, LiteralLexerToken)

        # Assert the read content matches the written content.
        assert first_token.content == content

    def test_lex_file_empty_line(self):
        """Test that lexing works with or without a trailing empty line."""
        file_name = "test_lex_file_empty_line.word"

        content_empty_line = "2\n"
        content_no_empty_line = "2"

        # Test token with empty line
        tokens = self._lex_from_file(file_name, content_empty_line)
        first_token = next(tokens)
        assert isinstance(first_token, LiteralLexerToken)

        # Test token without empty line
        tokens = self._lex_from_file(file_name, content_no_empty_line)
        first_token = next(tokens)
        assert isinstance(first_token, LiteralLexerToken)

    def test_lex_line(self):
        words = iter([Word("2", DebugData(0)), Word("TEST_VAR", DebugData(0))])
        lexer = Lexer()

        tokens = lexer.lex_line(words)
        literal = next(tokens)
        identifier = next(tokens)

        # Assert words get properly tokenized.
        assert isinstance(identifier, IdentLexerToken)
        assert isinstance(literal, LiteralLexerToken)

        words = iter([Word("#", DebugData(0)), Word("TEST_VAR", DebugData(0))])
        tokens = lexer.lex_line(words)

        # Assert tokens don't get tokenized
        with pytest.raises(StopIteration):
            next(tokens)

        # Assert empty lines are supported.
        with pytest.raises(StopIteration):
            next(lexer.lex_line(iter([])))

    def test_lex_word(self):
        # Test all subclasses of lexer tokens can be tokenized.
        lexer = Lexer()

        def assert_lexer_token_type(lexer: Lexer, token_type: Type[LexerToken]):
            word = Word(token_type.Types.values()[0], DebugData(0))
            assert isinstance(lexer.lex_word(word), token_type)

        for token_type in LexerToken.__subclasses__():
            assert_lexer_token_type(lexer, token_type)
