from pathlib import Path
from typing import Callable, Dict, List, Type, Iterator
import uuid

from words.compiler.compile_util import M0Util as m0
from words.lexer.lex import Lexer
from words.parser.parse import Parser
from words.parser.parse_util import Program
from words.token_types.lexer_token import LexerToken
from words.token_types.parser_token import ParserToken, VariableParserToken, FunctionParserToken, NumberParserToken, \
    IdentParserToken, MacroParserToken, BooleanOperatorParserToken, IfParserToken, ReturnParserToken


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
    def _compile_function_token(function_token: FunctionParserToken) -> str:
        output = ""
        func_end = function_token.name + "_end"
        output += f"b {func_end}\n"
        output += f"{function_token.name}:\n"

        # Reserve parameters
        param_regs = {i + 4: prm.value for i, prm in enumerate(function_token.parameters)}
        output = output + m0.asm_instruction_list("pop", list(param_regs.keys()))

        for token in function_token.body:
            output += M0Compiler._compile_token(token, param_regs)

        output += f"{func_end}:\n"
        return output

    @staticmethod
    def _compile_number_token(token) -> str:
        return m0.asm_push_value_stack(token.value)

    @staticmethod
    def _compile_ident_token(token, used_regs) -> str:
        if token.value not in used_regs.values():
            # It must be a function (or some undefined identifier)
            return m0.asm_branch(token.value)
        # It is a parameter or variable
        reg_to_push: List[int] = [m0.reg_from_val(token.value, used_regs)]
        return m0.asm_instruction_list("push", reg_to_push)

    @staticmethod
    def _compile_boolean_op_token(token) -> str:
        output = ""

        output += m0.asm_instruction_list("pop", [0, 1])
        skip_false_if_true_branch = f"true_line{str(token.debug_data)}_{str(uuid.uuid4())[:8]}"
        false_branch = f"false_line{str(token.debug_data)}_{str(uuid.uuid4())[:8]}"
        # TODO: check what comparison instead of only bne
        output += m0.asm_instruction_move(0, 1)
        output += f"{m0.boolean_compile_map[token.value]} {skip_false_if_true_branch}\n"
        output += f"{false_branch}:\n"
        output += m0.asm_instruction_move(0, 0)
        output += f"{skip_false_if_true_branch}:\n"
        output += m0.asm_instruction_list("push", [0])

        return output

    @staticmethod
    def _compile_macro_token(token) -> str:
        return ""

    @staticmethod
    def _compile_if_token(token, used_regs) -> str:
        return ""

    @staticmethod
    def _compile_return_token(token, used_regs) -> str:
        return ""

    @staticmethod
    def _compile_token(token: ParserToken, used_regs: dict) -> str:
        if isinstance(token, FunctionParserToken):
            return M0Compiler._compile_function_token(token)
        elif isinstance(token, NumberParserToken):
            return M0Compiler._compile_number_token(token)
        elif isinstance(token, IdentParserToken):
            return M0Compiler._compile_ident_token(token, used_regs)
        elif isinstance(token, MacroParserToken):
            return M0Compiler._compile_macro_token(token)
        elif isinstance(token, BooleanOperatorParserToken):
            return M0Compiler._compile_boolean_op_token(token)
        elif isinstance(token, IfParserToken):
            return M0Compiler._compile_if_token(token, used_regs)
        elif isinstance(token, ReturnParserToken):
            return M0Compiler._compile_return_token(token, used_regs)
        raise RuntimeError(f"Cannot compile token {token.debug_str()}")

    @staticmethod
    def _compile_code_segment(ast: Program) -> str:
        dot_global = (
            ".global setup, loop\n\n"
        )
        code = ""
        for token in ast.tokens:
            code = code + M0Compiler._compile_token(token, {})

        setup = "setup: \n" + code

        return dot_global + setup + "loop: \n"

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
