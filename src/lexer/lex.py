from typing import Iterator
from pathlib import Path
from src.token_types.lexer_token import LexerToken, MacroLexerToken, KeywordLexerToken, LiteralLexerToken, DelimLexerToken, \
    OpLexerToken, IdentLexerToken

from src.lexer.lex_util import Word, DebugData


class Lexer:
    """Lexer, also known as a Tokenizer.

    Supplies functionality for reading text from a file and changing them into tokens the parser can accept.
    """
    @staticmethod
    def lex_file(file: Path) -> Iterator[LexerToken]:
        """
        Lex all tokens from a file.

        :param file: Path to the file to lex.
        :return: An iterator over lexer tokens.
        """
        words: Iterator[Iterator[Word]] = (Lexer._split_line_into_words(line_nr, line) for line_nr, line in
                                           enumerate(open(file, 'r').readlines()))
        return Lexer._exhaustive_lex(words)

    @staticmethod
    def lex_line(line: Iterator[Word]) -> Iterator[LexerToken]:
        """
        Lex all words from a line into tokens.

        :param line: An iterator over words to lex.
        :return: An iterator of lexer tokens.
        """
        try:
            token = Lexer.lex_word(next(line))
            if token.value == LiteralLexerToken.Types.COMMENT:
                return
            yield token
            yield from Lexer.lex_line(line)

        except StopIteration:
            return

    @staticmethod
    def lex_word(token: Word) -> LexerToken:
        """
        Lex a single word.

        :param token: The word to lex into a token.
        :return: A lexer token.
        """
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

    @staticmethod
    def _split_line_into_words(line_nr: int, line: str) -> Iterator[Word]:
        """
        Split a line into words.

        :param line_nr: The index of the line, used for debugging.
        :param line: The line to split.
        :return:
        """
        yield from (Word(word, DebugData(line_nr)) for word in line.split())

    @staticmethod
    def _exhaustive_lex(words: Iterator[Iterator[Word]]) -> Iterator[LexerToken]:
        """
        Lex tokens from iterator until it is empty.

        :param words: An iterator of iterators over words to lex.
        :return: An iterator of lexer tokens.
        """
        try:
            yield from Lexer.lex_line(iter(next(words)))
            yield from Lexer._exhaustive_lex(words)
        except StopIteration:
            return


# Debug main
if __name__ == '__main__':
    values = [token_.value for token_ in list(Lexer.lex_file(Path("../../examples/loop.word")))]
    print(len(values))
    assert len(values) == 31  # poor man's testcase
