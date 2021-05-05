from pprint import pprint
from typing import List, Iterator

from blocks.token.token import Token, MacroToken, KeywordToken, LiteralToken, DelimToken, OpToken, IdentToken


class Lexer:
    @staticmethod
    def lex_file(filepath):
        text: Iterator[Iterator[str]] = Lexer.split_lines_into_words(open(filepath, 'r').readlines())
        return Lexer.lex(text)

    @staticmethod
    def split_lines_into_words(lines: List[str]) -> Iterator[Iterator[str]]:
        yield from (line.split() for line in lines)

    @staticmethod
    def lex(words: Iterator[Iterator[str]]) -> Iterator[Token]:
        return Lexer.exhaustive_lex(words)

    @staticmethod
    def exhaustive_lex(text: Iterator[Iterator[str]]) -> Iterator[Token]:
        try:
            yield from Lexer.lex_line(iter(next(text)))
            yield from Lexer.exhaustive_lex(text)
        except StopIteration:
            return

    @staticmethod
    def lex_line(line: Iterator[str]) -> Iterator[Token]:
        try:
            token = Lexer.lex_token(next(line))
            if token.type == LiteralToken.Types.COMMENT:
                return
            yield token
            yield from Lexer.lex_line(line)

        except StopIteration:
            return

    @staticmethod
    def lex_token(token: str) -> Token:
        if token in DelimToken.Types.values():
            return DelimToken(token)
        if token in IdentToken.Types.values():
            return IdentToken(token)
        if token in KeywordToken.Types.values():
            return KeywordToken(token)
        if token in LiteralToken.Types.values():
            return LiteralToken(token)
        if token in MacroToken.Types.values():
            return MacroToken(token)
        if token in OpToken.Types.values():
            return OpToken(token)
        if token.isdigit():
            return LiteralToken(LiteralToken.Types.NUMBER.value)

        return IdentToken(IdentToken.Types.IDENTIFIER.value)


# Debug main
if __name__ == '__main__':
    values = [token_ for token_ in list(Lexer.lex_file("../../input/loop.ul"))]
    pprint(values)
    assert len(values) == 31  # poor mans testcase
