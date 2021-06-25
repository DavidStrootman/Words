from typing import List, Iterator, Tuple

from words.token.lexer_token import LexerToken, MacroLexerToken, KeywordLexerToken, LiteralLexerToken, DelimLexerToken, \
    OpLexerToken, IdentLexerToken

from words.lexer.lex_util import Word, DebugData


class Lexer:
    @staticmethod
    def lex_file(filepath):
        words: Iterator[Iterator[Word]] = (Lexer.split_line_into_words(line_nr, line) for line_nr, line in
                                           enumerate(open(filepath, 'r').readlines()))
        return Lexer.lex(words)

    @staticmethod
    def split_line_into_words(line_nr, line) -> Iterator[Word]:
        yield from (Word(word, DebugData(line_nr)) for word in line.split())

    @staticmethod
    def lex(words: Iterator[Iterator[Word]]) -> Iterator[LexerToken]:
        return Lexer.exhaustive_lex(words)

    @staticmethod
    def exhaustive_lex(words: Iterator[Iterator[Word]]) -> Iterator[LexerToken]:
        try:
            yield from Lexer.lex_line(iter(next(words)))
            yield from Lexer.exhaustive_lex(words)
        except StopIteration:
            return

    @staticmethod
    def lex_line(line: Iterator[Word]) -> Iterator[LexerToken]:
        try:
            token = Lexer.lex_token(next(line))
            if token.value == LiteralLexerToken.Types.COMMENT:
                return
            yield token
            yield from Lexer.lex_line(line)

        except StopIteration:
            return

    @staticmethod
    def lex_token(token: Word) -> LexerToken:
        if token.content in DelimLexerToken.Types.values():
            return DelimLexerToken(token)
        if token.content in KeywordLexerToken.Types.values():
            return KeywordLexerToken(token)
        if token.content in LiteralLexerToken.Types.values():
            return LiteralLexerToken(LiteralLexerToken.Types(token.content), token)
        if token.content in MacroLexerToken.Types.values():
            return MacroLexerToken(token)
        if token.content in OpLexerToken.Types.values():
            return OpLexerToken(token)
        if token.content.isdigit():
            return LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, token)

        return IdentLexerToken(token)


# Debug main
if __name__ == '__main__':
    values = [token_.value for token_ in list(Lexer.lex_file("../../input/loop.ul"))]
    print(len(values))
    assert len(values) == 31  # poor man's testcase
