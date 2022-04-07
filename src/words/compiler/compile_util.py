class M0Util:
    @staticmethod
    def asm_instruction_load(dest_reg: int, immed32: int):
        return f"ldr {dest_reg}, ={immed32}\n"

    @staticmethod
    def asm_instruction_move(dest_reg: int, immed8: int):
        return f"mov {dest_reg}, #{immed8}\n"

    @staticmethod
    def asm_instruction_one_reg(inst: str, reg1: int, immed: int):
        return f"{inst} {reg1}"

    @staticmethod
    def asm_instruction_two_reg(inst: str, reg1: int, reg2: int):
        return f"{inst} {reg1}, {reg2}"

    @staticmethod
    def asm_instruction_list(inst: str, regs: list[int]):
        regs_str = ", ".join([f"r{str(reg)}" for reg in regs])
        return f"{inst} {{{regs_str}}}\n"

    @staticmethod
    def reg_from_val(ident_val: str, used_regs: dict) -> int:
        index = list(used_regs.values()).index(ident_val)
        return index

    boolean_compile_map = {
        "==": "beq",
        "!=": "bne",
        ">=": "bge",
        "<=": "bls",
        ">": "bgt",
        "<": "blt",
    }
