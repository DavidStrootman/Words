from typing import Dict, List, Tuple, Optional


def execute_program(program: "Program") -> Optional[any]:
    """
    Execute a program.

    :param program: The program to execute. This function is used internally by the interpreter, but can be called
     directly.
    :return: The return value of the program executed, if any.
    """
    global_stack = list()
    dictionary = dict()
    result: Tuple[List, Dict] = exhaustive_interpret_tokens(program.tokens, global_stack, dictionary)

    return _return_value_or_none(result)


def _return_value_or_none(result: Tuple[List, Dict]) -> Optional[any]:
    """
    Returns the value from result, or None if it has no return value
    :param result: the result of an Interpreted program.
    :return: Any value returned by the program or None
    """
    if len(result[0]) > 0:
        return result[0][-1]
    return None


def exhaustive_interpret_tokens(tokens_: List["ParserToken"], stack_: list, dictionary_: dict) -> Tuple[list, dict]:
    """
    Interpret tokens from list until it is empty.

    :param tokens_: The tokens to interpret.
    :param stack_: The stack to use for interpreting.
    :param dictionary_: The dictionary to use for interpreting.
    :return: The resulting stack and dictionary after interpreting.
    """
    if tokens_:
        return exhaustive_interpret_tokens(tokens_[1:], *tokens_[0].execute(stack_, dictionary_))
    return stack_, dictionary_
