from pprint import pprint
from typing import List, Iterator
from blocks.token.token import MacroType, Token, TokenType
from itertools import chain


class Lexer:
    def split_lines_into_words(self, lines: List[str]) -> Iterator[List[str]]:
        yield from (line.split() for line in lines)

    def lex_file(self, filepath):
        text: Iterator[List[str]] = self.split_lines_into_words(open(filepath, 'r').readlines())
        return self.exhaustive_lex(text)

    def lex_line(self, line: List[str]) -> Iterator[Token]:
        return [self.lex_token(token) for token in line]

    def lex_token(self, token: str) -> Token:
        if token in TokenType.values():
            return Token(token_type=TokenType(token))
        if token in MacroType.values():
            return Token(token_type=MacroType(token))
        if token.isdigit():
            return Token(token_type=TokenType.NUMBER)

        return Token(token_type=TokenType.LITERAL)

    def exhaustive_lex(self, text: Iterator[List[str]]):
        try:
            yield self.lex_line(next(text))
            yield from self.exhaustive_lex(text)
        except StopIteration:
            pass


# Debug main
if __name__ == '__main__':
    pprint([token.type.name for token in chain.from_iterable(Lexer().lex_file("../../input/loop.ul"))])