from pprint import pprint
from typing import Iterator


from blocks.lexer.lex import Lexer
from blocks.token.token import LexerToken


class AST:
    def __init__(self, tokens):
        self.tokens = tokens


class Parser:
    @staticmethod
    def parse(tokens: Iterator[LexerToken]):
        parsed_tokens = Parser.parse_exhaustive(tokens)
        ast = AST(parsed_tokens)
        return ast

    @staticmethod
    def parse_exhaustive(tokens: Iterator[LexerToken]):
        try:
            return [next(tokens).parse(tokens)] + Parser.parse_exhaustive(tokens)
        except StopIteration:
            return []


if __name__ == '__main__':
    lexed_tokens_ = Lexer.lex_file("../../input/loop.ul")
    AST = Parser.parse(lexed_tokens_)
    x = 5
