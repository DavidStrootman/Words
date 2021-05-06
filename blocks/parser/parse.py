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
            yield next(tokens).parse(tokens)
            yield from Parser.parse_exhaustive(tokens)
        except StopIteration:
            return


if __name__ == '__main__':
    lexed_tokens_ = Lexer.lex_file("../../input/loop.ul")
    parsed_tokens_ = Parser.parse(lexed_tokens_)
    teet = list(parsed_tokens_.tokens)
    x = 5
