from typing import List, Iterator

from words.token.lexer_token import LexerToken, MacroLexerToken, KeywordLexerToken, LiteralLexerToken, DelimLexerToken, OpLexerToken, IdentLexerToken


class Lexer:
    @staticmethod
    def lex_file(filepath):
        text: Iterator[Iterator[str]] = Lexer.split_lines_into_words(open(filepath, 'r').readlines())
        return Lexer.lex(text)

    @staticmethod
    def split_lines_into_words(lines: List[str]) -> Iterator[Iterator[str]]:
        yield from (line.split() for line in lines)

    @staticmethod
    def lex(words: Iterator[Iterator[str]]) -> Iterator[LexerToken]:
        return Lexer.exhaustive_lex(words)

    @staticmethod
    def exhaustive_lex(text: Iterator[Iterator[str]]) -> Iterator[LexerToken]:
        try:
            yield from Lexer.lex_line(iter(next(text)))
            yield from Lexer.exhaustive_lex(text)
        except StopIteration:
            return

    @staticmethod
    def lex_line(line: Iterator[str]) -> Iterator[LexerToken]:
        try:
            token = Lexer.lex_token(next(line))
            if token.value == LiteralLexerToken.Types.COMMENT:
                return
            yield token
            yield from Lexer.lex_line(line)

        except StopIteration:
            return

    @staticmethod
    def lex_token(token: str) -> LexerToken:
        if token in DelimLexerToken.Types.values():
            return DelimLexerToken(token)
        if token in KeywordLexerToken.Types.values():
            return KeywordLexerToken(token)
        if token in LiteralLexerToken.Types.values():
            return LiteralLexerToken(LiteralLexerToken.Types(token), token)
        if token in MacroLexerToken.Types.values():
            return MacroLexerToken(token)
        if token in OpLexerToken.Types.values():
            return OpLexerToken(token)
        if token.isdigit():
            return LiteralLexerToken(LiteralLexerToken.Types.NUMBER.value, token)

        return IdentLexerToken(token)


# Debug main
if __name__ == '__main__':
    values = [token_.value for token_ in list(Lexer.lex_file("../../input/loop.ul"))]
    print(len(values))
    assert len(values) == 31  # poor man's testcase
