from time import perf_counter
from typing import Iterator
import sys

from input.loop import run as run_python
from words.lexer.lex import Lexer
from words.parser.parse import Parser
from words.token.lexer_token import LexerToken
from words.interpreter.interpret import Interpreter

if __name__ == '__main__':
    sys.setrecursionlimit(4000)

    interpret_start = perf_counter()

    lexed_tokens: Iterator[LexerToken] = Lexer.lex_file("input/loop.ul")

    program = Parser.parse(lexed_tokens)

    interpreter_result = Interpreter.interpret(program)

    interpret_end = perf_counter()
    print(f"Time elapsed during interpreting: {interpret_end - interpret_start}")

    python_result = run_python()

    try:
        assert interpreter_result == python_result
    except AssertionError:
        raise RuntimeError(
            f"Mismatch in results between words and python. Words: {interpreter_result}, Python: {python_result}")
