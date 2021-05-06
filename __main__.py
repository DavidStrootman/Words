from typing import Iterator

from blocks.lexer.lex import Lexer
from blocks.parser.parse import Parser
from blocks.token.token import LexerToken


if __name__ == '__main__':
    lexed_tokens: Iterator[LexerToken] = Lexer.lex_file("input/loop.ul")
    parsed_tokens = Parser.parse(lexed_tokens)
