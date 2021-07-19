from typing import List, Tuple


def execute_program(program: "Program") -> any:
    global_stack = list()
    dictionary = dict()
    result = exhaustive_interpret_tokens(program.tokens, global_stack, dictionary)
    if len(result[0]) > 0:
        return result[0][-1]
    return None


def exhaustive_interpret_tokens(tokens_: List["ParserToken"], stack_: list, dictionary_: dict) -> Tuple[list, dict]:
    if tokens_:
        return exhaustive_interpret_tokens(tokens_[1:], *tokens_[0].execute(stack_, dictionary_))
    return stack_, dictionary_
