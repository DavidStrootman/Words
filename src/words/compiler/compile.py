from pathlib import Path
from typing import Callable, Dict, List, Iterator
import uuid

from words.compiler.compile_util import M0Util as m0
from words.lexer.lex import Lexer
from words.parser.parse import Parser
from words.parser.parse_util import Program
from words.token_types.lexer_token import LexerToken
from words.token_types.parser_token import ParserToken, VariableParserToken, FunctionParserToken, NumberParserToken, \
    IdentParserToken, MacroParserToken, BooleanOperatorParserToken, IfParserToken, ReturnParserToken, \
    ArithmeticOperatorParserToken, BooleanParserToken, WhileParserToken, CopyParserToken


class Compiler:
    """
    The compiler is used to compile the code to run natively on a piece of hardware.
    The only supported assembly is Cortex M0.
    """

    @staticmethod
    def compile(ast: Program, target: str) -> str:
        """
        Compile a program.

        :param ast: The AST to compile.
        :param target: What platform to compile for.
        :return: The compiled assembly.
        """
        selected_target = target.lower()

        if selected_target not in platform_compilers:
            raise NotImplementedError(f"{target:} not supported")

        return platform_compilers[selected_target](ast)

    @staticmethod
    def build_asm(sections: List[str]) -> str:
        """
        Join all assembly sections into a complete program.
        :param sections: The sections to join.
        :return: Joined sections as a string.
        """
        return "\n".join(sections) + "\n"

    @staticmethod
    def compile_file(file_path: Path, target: str) -> str:
        """
        Compile from a file, this is the most common entrypoint for the Compiler.

        :param file_path: Path to the file to interpret.
        :param target: The platform to compile for.
        :return: The return value of the program executed, if any.
        """
        lexed_tokens: Iterator[LexerToken] = Lexer.lex_file(file_path)

        program = Parser.parse(lexed_tokens)

        return Compiler.compile(program, target)


class M0Compiler:
    @staticmethod
    def _compile_directives(ast: Program):
        """
        Compile M0 Directives.
        :param ast: The ast to compile from.
        :return: The M0 directives.
        """
        return ".cpu cortex-m0\n.align 2\n.text\n"

    @staticmethod
    def _compile_bss_segment(ast: Program) -> str:
        """
        Compile the M0 Bss segment.
        :param ast: The ast to compile from
        :return: The compiled Bss segment.
        """
        bytes_to_reserve = len(Compiler.find_token_in_ast(ast.tokens, VariableParserToken))

        bss_segment = (
            ".bss \n"
            ".byte " + ",".join(["0" for byte in range(bytes_to_reserve)]) + "\n"
                                                                             ".byte 0")

        return bss_segment

    @staticmethod
    def _compile_function_token(function_token: FunctionParserToken) -> str:
        """
        Compile a function token.

        :param function_token: The token to compile from.
        :return: The Compiled token.
        """
        output = ""
        func_end = function_token.name + "_end"
        output += "\n"
        output += m0.asm_comment(f"Start of function {function_token.name} at line {function_token.debug_data.line}")
        output += f"b {func_end} \n"
        output += f"{function_token.name}:\n"

        param_regs = {}
        # Reserve parameters
        if function_token.parameters:
            param_regs = {i + 3: prm.value for i, prm in enumerate(function_token.parameters)}
            output += m0.asm_instruction_move_lr_into(5)
            for reg in param_regs.keys():
                output += m0.asm_instruction_move_reg(reg - 2, reg)
            output += m0.asm_instruction_list("pop", list(param_regs.keys()))

            output += m0.asm_instruction_list("push", [5])
            output += m0.asm_instruction_list("push", [reg - 2 for reg in list(param_regs.keys())])
            output += "\n"
        else:
            output += m0.asm_push_lr() + "\n"

        output += m0.asm_comment("Function body:")
        output += "".join(M0Compiler._compile_token(token, param_regs) for token in function_token.body)

        # r6 holds return, r7 holds lr
        output += "\n"
        output += m0.asm_comment("Function end cleanup:")
        output += m0.asm_comment("return value, assuming function solves:")
        output += m0.asm_instruction_list("pop", [6])
        output += m0.asm_instruction_list("pop", list(param_regs.keys()))
        output += m0.asm_comment("link register:")
        output += m0.asm_instruction_list("pop", [7])
        # Place output on stack
        output += m0.asm_instruction_list("push", [6])

        output += m0.asm_instruction_move_into_pc(7)

        output += f"{func_end}:\n"
        output += m0.asm_comment(f"End of function {function_token.name} at line {function_token.debug_data.line}\n")

        return output

    @staticmethod
    def _compile_number_token(token) -> str:
        """
        Compile a number token.

        :param token: The token to compile from.
        :return: The Compiled token.
        """
        return m0.asm_push_value_stack(token.value)

    @staticmethod
    def _compile_ident_token(token, used_regs) -> str:
        """
        Compile an identifier.

        :param token: The token to compile from.
        :param used_regs: The registers that are already in use.
        :return: The Compiled token.
        """
        output = ""

        if token.value not in used_regs.values():
            # It must be a function (or some undefined identifier)
            output += m0.asm_branch_link(token.value)
        else:
            # It is a parameter or variable
            reg_to_push: List[int] = [m0.reg_from_val(token.value, used_regs)]
            output += m0.asm_instruction_list("push", reg_to_push)

        return output

    @staticmethod
    def _compile_boolean_op_token(token) -> str:
        """
        Compile a boolean operator.

        :param token: The token to compile from.
        :return: The Compiled token.
        """
        output = ""

        output += m0.asm_instruction_list("pop", [1, 2])
        skip_false_if_true_branch = f"true_line{str(token.debug_data)}_{str(uuid.uuid4())[:8]}"
        false_branch = f"false_line{str(token.debug_data)}_{str(uuid.uuid4())[:8]}"
        output += m0.asm_instruction_move(dest_reg=0, immed8=1)
        output += m0.asm_instruction_cmp_reg(2, 1)
        output += f"{m0.boolean_compile_map[token.value]} {skip_false_if_true_branch}\n"
        output += f"{false_branch}:\n"
        output += m0.asm_instruction_move(dest_reg=0, immed8=0)
        output += f"{skip_false_if_true_branch}:\n"
        output += m0.asm_instruction_list("push", [0])

        return output

    @staticmethod
    def _compile_macro_token(token: MacroParserToken) -> str:
        """
        Compile a macro.

        :param token: The token to compile from.
        :return: The Compiled token
        """
        output = ""
        if token.function_name == "__PRINT__":
            output += m0.asm_instruction_list("pop", [0])
            output += m0.asm_branch_link("print_num")
            output += m0.asm_instruction_list("push", [0])

        return output

    @staticmethod
    def _compile_if_token(if_token, used_regs) -> str:
        """
        Compile an if statement.

        :param if_token: The token to compile from.
        :param used_regs: The registers already in use.
        :return: The Compiled token.
        """
        output = ""
        if_uuid = str(uuid.uuid4())[:8]
        else_branch = f"else_body_of_if_on_line{str(if_token.debug_data)}_{if_uuid}"
        end_of_if = f"end_if_on_line{str(if_token.debug_data)}_{if_uuid}"

        output += m0.asm_instruction_list("pop", [0])
        output += m0.asm_instruction_cmp_immed(0, 0)
        output += f"beq {else_branch}\n"
        output += f"if_body_of_if_on_line{str(if_token.debug_data)}_{if_uuid}:\n"
        output += "".join(M0Compiler._compile_token(token, used_regs) for token in if_token.if_body)
        output += m0.asm_branch(end_of_if)

        output += f"{else_branch}:\n"
        output += "".join(M0Compiler._compile_token(token, used_regs) for token in if_token.else_body)
        output += f"{end_of_if}:\n"
        return output

    @staticmethod
    def _compile_return_token(token, used_regs) -> str:
        """
        Compile a return statement.

        :param token: The token to compile from.
        :param used_regs: The registers already in use.
        :return: The Compiled token
        """
        return ""

    @staticmethod
    def _compile_copy_token(token, used_regs) -> str:
        """
        Compile a copy statement.
        :param token: The token to compile from.
        :param used_regs: The registers already in use.
        :return: The Compiled token.
        """
        output = ""

        output += m0.asm_instruction_list("pop", [0])
        output += m0.asm_instruction_list("push", [0])
        output += m0.asm_instruction_list("push", [0])
        return output

    @staticmethod
    def _compile_boolean_token(token: BooleanParserToken) -> str:
        """
        Compile a boolean.

        :param token: The token to compile from.
        :return: The Compiled token
        """
        if token.value is True:
            return m0.asm_push_value_stack(1)
        return m0.asm_push_value_stack(0)

    @staticmethod
    def _compile_while_token(while_token: WhileParserToken, used_regs: dict) -> str:
        """
        Compile a while loop.
        :param while_token: The token to compile from.
        :param used_regs: The registers already in use.
        :return: The Compiled token.
        """
        output = ""
        while_uuid = str(uuid.uuid4())[:8]
        while_predicate = f"while_predicate_on_line{str(while_token.debug_data)}_{while_uuid}"
        while_body_start = f"while_body_on_line{str(while_token.debug_data)}_{while_uuid}"
        end_of_while = f"end_while_on_line{str(while_token.debug_data)}_{while_uuid}"

        # Predicate
        output += f"{while_predicate}:\n"
        output += "".join(M0Compiler._compile_token(token, used_regs) for token in while_token.predicate)
        output += m0.asm_instruction_list("pop", [0])
        output += m0.asm_instruction_cmp_immed(0, 0)
        output += f"beq {end_of_while}\n"

        # While body
        output += f"{while_body_start}:\n"
        output += "".join(M0Compiler._compile_token(token, used_regs) for token in while_token.statements)
        output += m0.asm_branch(while_predicate)
        output += f"{end_of_while}:\n"
        return output

    @staticmethod
    def _compile_arithmetic_op_token(token) -> str:
        """
        Compile an arithmetic operator.
        :param token: The token to compile from.
        :return: The Compiled token.
        """
        output = ""

        # Pop 2 values
        output += m0.asm_instruction_list("pop", [0, 1])
        # Do some arithmetic
        output += f"{m0.arithmetic_compile_map[token.value]} {m0.reg(0)}, {m0.reg(1)}, {m0.reg(0)}\n"
        # Push the new value
        output += m0.asm_instruction_list("push", [0])

        return output

    @staticmethod
    def _compile_token(token: ParserToken, used_regs: dict) -> str:
        """
        Compile a parser token into M0 Assembly.
        :param token: The token to compile from.
        :param used_regs: The registers already in use.
        :return: The Compiled token.
        """
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
        elif isinstance(token, ArithmeticOperatorParserToken):
            return M0Compiler._compile_arithmetic_op_token(token)
        elif isinstance(token, BooleanParserToken):
            return M0Compiler._compile_boolean_token(token)
        elif isinstance(token, WhileParserToken):
            return M0Compiler._compile_while_token(token, used_regs)
        elif isinstance(token, CopyParserToken):
            return M0Compiler._compile_copy_token(token, used_regs)

        raise RuntimeError(f"Cannot compile token {token.debug_str()}")

    @staticmethod
    def _compile_code_segment(ast: Program) -> str:
        """
        Compile the Code segment.
        :param ast: The AST to compile from.
        :return: Compiled Code segment.
        """
        dot_global = (
            ".global setup, loop\n\n"
        )
        code = ""
        functions = []
        for token in ast.tokens:
            if isinstance(token, FunctionParserToken):
                functions = functions + [M0Compiler._compile_token(token, {})]
            else:
                code = code + M0Compiler._compile_token(token, {})

        unittest = "mov r0, #2\n" \
                   "mov r1, #1\n" \
                   "bl a_unittest \n\n"

        setup = "setup: \n" + m0.asm_branch_link("serial_begin") + unittest + code + "\n\n".join(functions)

        return dot_global + setup + "loop: \nb loop\n "

    @staticmethod
    def compile(ast: Program) -> str:
        """
        Compile a program from an AST.
        :param ast: The parsed AST.
        :return: The complete M0 Assembly.
        """
        cpu_directive = M0Compiler._compile_directives(ast)
        # bss_segment = M0Compiler._compile_bss_segment(ast)
        code_segment = M0Compiler._compile_code_segment(ast)

        return Compiler.build_asm(
            [
                cpu_directive,
                # bss_segment,
                code_segment
            ]
        )


platform_compilers: Dict[str, Callable[[Program], str]] = {
    "cortex-m0": M0Compiler.compile
}
