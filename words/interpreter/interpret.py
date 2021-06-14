from words.parser.parse import Program
from words.interpreter.interpret_util import execute_program


class Interpreter:
    @staticmethod
    def interpret(program: Program):
        return execute_program(program)
