from abc import ABC
from pathlib import Path
from typing import Callable, Dict, List, Type, Iterator

from words.lexer.lex import Lexer
from words.parser.parse import Parser
from words.parser.parse_util import Program
from words.token_types.lexer_token import LexerToken
from words.token_types.parser_token import ParserToken, VariableParserToken


class Compiler:
    """
    The compiler is used to compile the code to run natively on a piece of hardware.
    The only supported hardware is the Arduino Due.
    """

    @staticmethod
    def compile(ast: Program, target: str = "arduino_due") -> str:
        selected_target = target.lower()

        if selected_target not in platform_compilers:
            raise NotImplementedError(f"{target:} not supported")
        
        return platform_compilers[target](ast)

    @staticmethod
    def build_asm(sections: List[str]) -> str:
        return "\n".join(sections) + "\n"

    @staticmethod
    def find_token_in_ast(ast: List[ParserToken], token: Type[ParserToken]) -> List[ParserToken]:
        """Recursively find token in ast tree"""
        def _find_token_in_token(token: Type[ParserToken]) -> ParserToken:
            pass
        return [_find_token_in_token(token)]

    @staticmethod
    def compile_file(file_path: Path) -> str:
        """
        Compile from a file, this is the most common entrypoint for the Compiler.

        :param file_path: Path to the file to interpret.
        :return: The return value of the program executed, if any.
        """
        lexed_tokens: Iterator[LexerToken] = Lexer.lex_file(file_path)

        program = Parser.parse(lexed_tokens)

        return Compiler.compile(program)


class M0Compiler:
    @staticmethod
    def _compile_cpu_directive():
        return ".cpu cortex-m0"

    @staticmethod
    def _compile_bss_segment(ast: Program):
        bytes_to_reserve = len(Compiler.find_token_in_ast(ast.tokens, VariableParserToken))
        
        bss_segment = f".bss \n" \
                      f".byte " + ",".join(["0" for byte in range(bytes_to_reserve)]) + "\n" \
                      f"test:\n" \
                      f".byte 0"

        return bss_segment

    @staticmethod
    def compile(ast: Program):

        cpu_directive = M0Compiler._compile_cpu_directive()
        bss_segment = M0Compiler._compile_bss_segment(ast)

        return Compiler.build_asm(
            [
                cpu_directive,
                bss_segment
            ]
        )


platform_compilers: Dict[str, Callable[[Program], str]] = {
    "arduino_due": M0Compiler.compile
}
