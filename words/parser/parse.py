from typing import Iterator

from words.lexer.lex import Lexer
from words.token.lexer_token import LexerToken
from words.parser.parse_util import Program


class Parser:
    @staticmethod
    def parse(tokens: Iterator[LexerToken]) -> Program:
        parsed_tokens = Parser.parse_exhaustive(tokens)
        program = Program(parsed_tokens)
        return program

    @staticmethod
    def parse_exhaustive(tokens: Iterator[LexerToken]):
        try:
            return [next(tokens).parse(tokens)] + Parser.parse_exhaustive(tokens)
        except StopIteration:
            return []


if __name__ == '__main__':
    lexed_tokens_ = Lexer.lex_file("../../input/loop.ul")
    program_ = Parser.parse(lexed_tokens_)
    yeet = 2
