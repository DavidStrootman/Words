class M0Util:
    @staticmethod
    def asm_reg(reg: int):
        return f"r{reg}"

    @staticmethod
    def asm_instruction_load(dest_reg: int, immed32: int):
        return f"ldr {M0Util.asm_reg(dest_reg)}, ={immed32}\n"

    @staticmethod
    def asm_instruction_move(dest_reg: int, immed8: int):
        return f"mov {M0Util.asm_reg(dest_reg)}, #{immed8}\n"

    @staticmethod
    def asm_instruction_one_reg(inst: str, reg1: int):
        return f"{inst} {M0Util.asm_reg(reg1)}"

    @staticmethod
    def asm_instruction_two_reg(inst: str, reg1: int, reg2: int):
        return f"{inst} {M0Util.asm_reg(reg1)}, {M0Util.asm_reg(reg2)}"

    @staticmethod
    def asm_instruction_list(inst: str, regs: list[int]):
        regs_str = ", ".join([M0Util.asm_reg(reg) for reg in regs])
        return f"{inst} {{{regs_str}}}\n"

    @staticmethod
    def asm_push_value_stack(value: int) -> str:
        output = ""
        if value > 0x11111111:
            output += M0Util.asm_instruction_load(0, value)
        output += M0Util.asm_instruction_move(0, value)
        output += M0Util.asm_instruction_list("push", [0])

        return output

    @staticmethod
    def asm_branch(target: str) -> str:
        return f"b {target}\n"

    @staticmethod
    def reg_from_val(ident_val: str, used_regs: dict) -> int:
        index = list(used_regs.values()).index(ident_val) + 4
        return index

    boolean_compile_map = {
        "==": "beq",
        "!=": "bne",
        ">=": "bge",
        "<=": "bls",
        ">": "bgt",
        "<": "blt",
    }
