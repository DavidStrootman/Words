from pathlib import Path
from typing import Optional, Iterator

from words.interpreter.interpret_util import execute_program
from words.lexer.lex import Lexer
from words.parser.parse import Program, Parser
from words.token_types.lexer_token import LexerToken


class Interpreter:
    """The Interpreter class is used to for interpreting a Words program."""
    @staticmethod
    def interpret(program: Program) -> Optional[any]:
        """
        Interpret a program.

        :param program: The program to interpret.
        :return: The return value of the program executed, if any.
        """
        return execute_program(program)

    @staticmethod
    def interpret_file(file_path: Path) -> Optional[any]:
        """
        Interpret from a file, this is the most common entrypoint for the interpreter.

        :param file_path: Path to the file to interpret.
        :return:  The return value of the program executed, if any.
        """
        lexed_tokens: Iterator[LexerToken] = Lexer.lex_file(file_path)

        program = Parser.parse(lexed_tokens)

        return Interpreter.interpret(program)
