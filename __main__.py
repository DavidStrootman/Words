from typing import Iterator
import sys

from words.lexer.lex import Lexer
from words.parser.parse import Parser
from words.token.lexer_token import LexerToken
from words.interpreter.interpret import Interpreter

if __name__ == '__main__':
    sys.setrecursionlimit(4000)

    lexed_tokens: Iterator[LexerToken] = Lexer.lex_file("input/fibonacci.ul")

    program = Parser.parse(lexed_tokens)

    interpreter_result = Interpreter.interpret(program)

    # TODO: unit testing and integration testing with python counterpart
