from pathlib import Path
from typing import Optional, Iterator, List

from words.interpreter.interpret_util import execute_program
from words.lexer.lex import Lexer
from words.parser.parse import Program, Parser
from words.token_types.lexer_token import LexerToken


class Interpreter:
    """The Interpreter class is used to for interpreting a Words program."""

    @staticmethod
    def interpret(program: Program, init: List) -> Optional[any]:
        """
        Interpret a program.

        :param program: The program to interpret.
        :param init: The initial values to place on the stack.
        :return: The return value of the program executed, if any.
        """
        if not init:
            init = []

        return execute_program(program, init=init)

    @staticmethod
    def interpret_file(file_path: Path, init: list) -> Optional[any]:
        """
        Interpret from a file, this is the most common entrypoint for the interpreter.

        :param file_path: Path to the file to interpret.
        :param init: The initial values to place on the stack.
        :return:  The return value of the program executed, if any.
        """
        if not init:
            init = []

        lexed_tokens: Iterator[LexerToken] = Lexer.lex_file(file_path)

        program = Parser.parse(lexed_tokens)

        return Interpreter.interpret(program, init=init)
