from typing import Optional

from words.parser.parse import Program
from words.interpreter.interpret_util import execute_program


class Interpreter:
    """The Interpreter class is used to for interpreting a Words program."""
    @staticmethod
    def interpret(program: Program) -> Optional[any]:
        """
        Interpret a program.

        :param program: The program to interpret
        :return: The return value of the program executed, if any.
        """
        return execute_program(program)
