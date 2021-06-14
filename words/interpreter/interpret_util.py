from typing import List, Tuple


def execute_program(program: "Program") -> int:
    global_stack = list()
    dictionary = dict()
    return exhaustive_interpret_tokens(program.tokens, global_stack, dictionary)[0][-1]


def exhaustive_interpret_tokens(tokens_: List["ParserToken"], stack_: list, dictionary_: dict) -> Tuple[
    list, dict]:
    if tokens_:
        return exhaustive_interpret_tokens(tokens_[1:], *tokens_[0].execute(stack_, dictionary_))
    return stack_, dictionary_
