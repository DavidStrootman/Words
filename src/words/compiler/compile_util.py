from typing import Optional


class M0Util:
    @staticmethod
    def reg(reg: int):
        return f"r{reg}"

    @staticmethod
    def asm_instruction_load(dest_reg: int, immed32: int):
        return f"ldr {M0Util.reg(dest_reg)}, ={immed32}\n"

    @staticmethod
    def asm_instruction_move(dest_reg: int, immed8: int):
        return f"mov {M0Util.reg(dest_reg)}, #{immed8}\n"

    @staticmethod
    def asm_instruction_move_reg(dest_reg: int, from_reg: int) -> str:
        return f"mov {M0Util.reg(dest_reg)}, {M0Util.reg(from_reg)}\n"

    @staticmethod
    def asm_instruction_move_into_pc(reg: int):
        return f"mov pc, {M0Util.reg(reg)}\n"

    @staticmethod
    def asm_instruction_move_lr_into(reg: int):
        return f"mov {M0Util.reg(reg)}, lr\n"

    @staticmethod
    def asm_instruction_cmp_immed(cmp_reg: int, immed8: int):
        return f"cmp {M0Util.reg(cmp_reg)}, #{immed8}\n"

    @staticmethod
    def asm_instruction_cmp_reg(cmp_reg: int, cmp_reg2: int):
        return f"cmp {M0Util.reg(cmp_reg)}, {M0Util.reg(cmp_reg2)}\n"

    @staticmethod
    def asm_instruction_one_reg(inst: str, reg1: int):
        return f"{inst} {M0Util.reg(reg1)}"

    @staticmethod
    def asm_instruction_two_reg(inst: str, reg1: int, reg2: int):
        return f"{inst} {M0Util.reg(reg1)}, {M0Util.reg(reg2)}"

    @staticmethod
    def asm_instruction_list(inst: str, regs: list[int]):
        regs_str = ", ".join([M0Util.reg(reg) for reg in regs])
        return f"{inst} {{ {regs_str} }}\n"

    @staticmethod
    def asm_push_lr() -> str:
        return "push { lr }\n"

    @staticmethod
    def asm_push_regs_lr(regs: list[int]) -> str:
        output = ""
        regs_str = ", ".join([M0Util.reg(reg) for reg in regs])
        output += "push { lr }\n"
        output += f"push {{ {regs_str} }}\n"

    @staticmethod
    def asm_pop_pc() -> str:
        return "pop { pc }\n"

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
    def asm_branch_link(target: str) -> str:
        return f"bl {target}\n"

    @staticmethod
    def asm_comment(comment: str) -> str:
        return f"@ {comment}\n"

    @staticmethod
    def asm_arithmetic(inst: str,
                       reg1: int,
                       reg2: int,
                       *,
                       reg3: Optional[int] = None,
                       immed3: Optional[int] = None,
                       immed8: Optional[int] = None):
        if not any(param is not None for param in [reg3, immed3, immed8]):
            raise RuntimeError("Expected some third parameter for asm arithmetic instruction.")
        if bool(reg3) + bool(immed3) + bool(immed8) > 1:
            raise RuntimeError("Too many keyword arguments for asm arithmetic instruction.")

        if reg3 is not None:
            return f"{inst}, {M0Util.reg(reg1)}, {M0Util.reg(reg2)}, {M0Util.reg(reg3)}"

        immed = immed3 if immed3 is not None else immed8
        return f"{inst}, {M0Util.reg(reg1)}, {M0Util.reg(reg2)}, #{immed}\n"

    @staticmethod
    def reg_from_val(ident_val: str, used_regs: dict) -> int:
        index = list(used_regs.values()).index(ident_val) + 3
        return index

    boolean_compile_map = {
        "==": "beq",
        "!=": "bne",
        ">=": "bge",
        "<=": "bls",
        ">": "bgt",
        "<": "blt",
    }

    arithmetic_compile_map = {
        "+": "add",
        "-": "sub"
    }
