from typing import Iterator, List
from src.lexer.lex import Lexer
from src.token_types.lexer_token import LexerToken
from src.parser.parse_util import Program


class Parser:
    """
    The Parser class is used to for parsing lexer tokens into a program the interpreter can interpret.
    """

    @staticmethod
    def parse(tokens: Iterator[LexerToken]) -> Program:
        """
        Parse an iterator of lexer tokens into a program.

        During the parsing step the simple lexer tokens are expanded with more information gotten from their context.

        :param tokens: An iterator over lexer tokens to parse.
        :return: A program.
        """
        parsed_tokens = Parser._parse_exhaustive(tokens)
        program = Program(parsed_tokens)
        return program

    @staticmethod
    def _parse_exhaustive(tokens: Iterator[LexerToken]) -> List["ParserToken"]:
        """
        parse parser tokens from iterator until it is empty.

        :param tokens: The lexer tokens parse.
        :return: List of parser tokens.
        """
        try:
            return [next(tokens).parse(tokens)] + Parser._parse_exhaustive(tokens)
        except StopIteration:
            return []


if __name__ == '__main__':
    lexed_tokens_ = Lexer.lex_file("../../examples/loop.word")
    program_ = Parser.parse(lexed_tokens_)
    yeet = 2
