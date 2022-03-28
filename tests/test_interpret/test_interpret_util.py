from typing import Iterator, List

from words.interpreter.interpret_util import execute_program, _return_value_or_none, exhaustive_interpret_tokens
from words.lexer.lex import Lexer
from words.parser.parse import Parser
from words.token_types.lexer_token import LexerToken
from words.token_types.parser_token import ParserToken


class TestInterpretUtil:
    def test_execute_program_positive(self):
        lexed_tokens: Iterator[LexerToken] = Lexer.lex_from_string("921")

        program = Parser.parse(lexed_tokens)

        assert execute_program(program, init=[]) == 921

    def test_return_value_or_none_value(self):
        assert _return_value_or_none(([20], {})) == 20

    def test_return_value_or_none_none(self):
        assert not _return_value_or_none(([], {}))

    def test_exhaustive_interpret_tokens(self):
        tokens: List[ParserToken] = Parser.parse(Lexer.lex_from_string("52 +")).tokens

        result = exhaustive_interpret_tokens(tokens, [921], {})

        assert result[0] == [921 + 52]
