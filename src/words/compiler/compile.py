from pathlib import Path
from typing import Callable, Dict, List, Type, Iterator

from words.lexer.lex import Lexer
from words.parser.parse import Parser
from words.parser.parse_util import Program
from words.token_types.lexer_token import LexerToken
from words.token_types.parser_token import ParserToken, VariableParserToken, FunctionParserToken, NumberParserToken, \
    IdentParserToken, MacroParserToken


class Compiler:
    """
    The compiler is used to compile the code to run natively on a piece of hardware.
    The only supported assembly is Cortex M0.
    """

    @staticmethod
    def compile(ast: Program, target: str) -> str:
        selected_target = target.lower()

        if selected_target not in platform_compilers:
            raise NotImplementedError(f"{target:} not supported")

        return platform_compilers[selected_target](ast)

    @staticmethod
    def build_asm(sections: List[str]) -> str:
        return "\n".join(sections) + "\n"

    @staticmethod
    def find_token_in_ast(ast: List[ParserToken], token: Type[ParserToken]) -> List[ParserToken]:
        """Recursively find token in ast tree"""

        def _find_token_in_token(token_: Type[ParserToken]) -> ParserToken:
            pass

        return [_find_token_in_token(token)]

    @staticmethod
    def compile_file(file_path: Path, target: str) -> str:
        """
        Compile from a file, this is the most common entrypoint for the Compiler.

        :param file_path: Path to the file to interpret.
        :return: The return value of the program executed, if any.
        """
        lexed_tokens: Iterator[LexerToken] = Lexer.lex_file(file_path)

        program = Parser.parse(lexed_tokens)

        return Compiler.compile(program, target)


class M0Compiler:
    @staticmethod
    def _compile_cpu_directive(ast: Program):
        return ".cpu cortex-m0"

    @staticmethod
    def _compile_bss_segment(ast: Program):
        bytes_to_reserve = len(Compiler.find_token_in_ast(ast.tokens, VariableParserToken))

        bss_segment = (
            ".bss \n"
            ".byte " + ",".join(["0" for byte in range(bytes_to_reserve)]) + "\n"
            "test:\n"
            ".byte 0")

        return bss_segment

    @staticmethod
    def _asm_instruction_list(inst: str, regs: list[int]):
        regs_str = ", ".join([f"r{str(reg)}" for reg in regs])
        return f"push {{{regs_str}}}\n"

    @staticmethod
    def _compile_function_token(token) -> str:
        output = ""
        used_registers = []
        # Reserve parameters
        used_registers = used_registers + list(range(len(token.parameters)))
        output = M0Compiler._asm_instruction_list("push", used_registers)
        x = 3


    @staticmethod
    def _compile_number_token(token) -> str:
        return ""

    @staticmethod
    def _compile_ident_token(token) -> str:
        return ""

    @staticmethod
    def _compile_macro_token(token) -> str:
        return ""

    @staticmethod
    def _compile_token(token: ParserToken) -> str:
        if isinstance(token, FunctionParserToken):
            return M0Compiler._compile_function_token(token)
        elif isinstance(token, NumberParserToken):
            return M0Compiler._compile_number_token(token)
        elif isinstance(token, IdentParserToken):
            return M0Compiler._compile_ident_token(token)
        elif isinstance(token, MacroParserToken):
            return M0Compiler._compile_macro_token(token)
        raise RuntimeError(f"Cannot compile token {token.debug_str()}")

    @staticmethod
    def _compile_code_segment(ast: Program) -> str:
        dot_global = (
            ".global setup, loop\n\n"
        )
        code = []
        for token in ast.tokens:
            code = code + [M0Compiler._compile_token(token)]
        code_segment = (
            dot_global + "setup: \n"
                         
            "loop: \n"
        )

        return code_segment

    @staticmethod
    def compile(ast: Program):
        cpu_directive = M0Compiler._compile_cpu_directive(ast)
        bss_segment = M0Compiler._compile_bss_segment(ast)
        code_segment = M0Compiler._compile_code_segment(ast)

        return Compiler.build_asm(
            [
                cpu_directive,
                bss_segment,
                code_segment
            ]
        )


platform_compilers: Dict[str, Callable[[Program], str]] = {
    "cortex-m0": M0Compiler.compile
}
