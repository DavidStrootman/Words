from typing import Iterator

from blocks.lexer.lex import Lexer
from blocks.token.token import Token

class Parser:
    @staticmethod
    def parse(tokens: Iterator[Token]):
        yield next(tokens).parse()




if __name__ == '__main__':
    lexed_tokens = Lexer.lex_file("../../input/loop.ul")
    parsed_tokens = Parser.parse()
