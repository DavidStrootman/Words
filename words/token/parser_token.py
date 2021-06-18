from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from words.interpreter.interpret_util import exhaustive_interpret_tokens


class ParserToken(ABC):
    """Base parser token."""
    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        raise RuntimeError(f"Tried to call unimplemented method \"execute\" on {self.__class__.__name__}.")


class DictionaryToken(ABC):
    """A visitable token that is stored in the dictionary."""
    class RemovedDictionaryToken:
        pass

    @abstractmethod
    def visit(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        pass


class NumberParserToken(ParserToken):
    def __init__(self, value: int):
        self.value = value

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        return stack + [self.value], dictionary


class BooleanParserToken(ParserToken):
    def __init__(self, value: bool):
        if value == "True":
            self.value = True
        if value == "False":
            self.value = False

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        return stack + [self.value], dictionary


class MacroParserToken(ParserToken):
    def __init__(self, function_name: str):
        self.function_name = function_name

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        if self.function_name == "__PRINT__":
            print(stack[-1])
            return stack, dictionary


class WhileParserToken(ParserToken):
    def __init__(self, predicate: List[ParserToken], statements: List[ParserToken]):
        self.predicate = predicate
        self.statements = statements

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        predicate_outcome: bool = exhaustive_interpret_tokens(self.predicate, stack, dictionary)[0][0]
        if predicate_outcome:
            return self.execute(*exhaustive_interpret_tokens(self.statements, stack, dictionary))
        return stack, dictionary


class IfParserToken(ParserToken):
    def __init__(self, if_body: List[ParserToken], else_body: Optional[List[ParserToken]] = None):
        self.if_body = if_body
        self.else_body = else_body

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        predicate = stack[-1]
        if predicate is True:
            return exhaustive_interpret_tokens(self.if_body, stack[:-1], dictionary)
        if self.else_body:
            return exhaustive_interpret_tokens(self.else_body, stack[:-1], dictionary)
        return stack[:-1], dictionary


class VariableParserToken(ParserToken, DictionaryToken):
    class VarUnassigned:
        pass

    def __init__(self, value: str):
        self.value: str = value
        self.assigned_value: any = self.VarUnassigned

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        if self.value in dictionary:
            raise KeyError(f"Variable {self.value} already exists in dictionary.")
        return stack, {**dictionary, **{self.value: self}}

    def visit(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        return stack + list([self.assigned_value]), dictionary


class ValueParserToken(ParserToken):
    def __init__(self, value: str):
        self.value = value

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        return stack + list([self.value]), dictionary


class IdentParserToken(ParserToken):
    def __init__(self, value: str):
        self.value = value

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        if self.value in dictionary:
            # TODO: Create generic get function for dictionary
            if isinstance(dictionary[self.value], FunctionParserToken):
                return dictionary[self.value].visit(stack, dictionary)
            else:
                return stack + [dictionary[self.value]], dictionary
        raise KeyError(f"Undefined function or variable {self.value} in dictionary.")


class ReturnParserToken(ParserToken):
    def __init__(self, count: int):
        self.count = count

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        return [stack[-1]], dictionary


class FunctionParserToken(ParserToken, DictionaryToken):
    def __init__(self, name, parameters: List[ValueParserToken], body: List[ParserToken]):
        self.name = name
        self.parameters: List[ValueParserToken] = parameters
        self.body = body

    def execute(self, stack: list, dictionary: dict):
        if self.name in dictionary:
            raise KeyError(f"Function {self.name} already exists in dictionary.")
        dictionary[self.name] = self
        return stack, dictionary

    def visit(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        return stack + exhaustive_interpret_tokens(self.body, *self.setup_parameters(stack, dictionary.copy()))[0], dictionary

    def setup_parameters(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        def rec_setup_parameters(stack_: list, dictionary_: dict, parameters: list):
            if not parameters:
                return stack_, dictionary_

            return rec_setup_parameters(stack_[:-1], {**dictionary, **{parameters[0].value: stack_[-1]}},
                                        parameters[1:])

        return rec_setup_parameters(stack, dictionary, self.parameters)


class ArithmeticOperatorParserToken(ParserToken):
    def __init__(self, value: str):
        self.value = value

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        topmost_value = stack[-1]
        second_value = stack[-2]

        if self.value == "+":
            return stack[:-2] + [second_value + topmost_value], dictionary
        if self.value == "-":
            return stack[:-2] + [second_value - topmost_value], dictionary
        # TODO: Create generic exception
        raise NotImplementedError(f"Unimplemented ArithmeticOperator {self.value}")


class BooleanOperatorParserToken(ParserToken):
    def __init__(self, value: str):
        self.value = value

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        if self.value == "==":
            topmost_value = stack[-1]
            second_value = stack[-2]
            return stack[:-2] + [second_value == topmost_value], dictionary
        if self.value == ">=":
            topmost_value = stack[-1]
            second_value = stack[-2]
            return stack[:-2] + [second_value >= topmost_value], dictionary
        raise NotImplementedError(f"Unimplemented BooleanOperator {self.value}")


class DictionaryOperatorParserToken(ParserToken):
    def __init__(self, value: str, variable_name: str):
        self.value = value
        self.variable_name = variable_name

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        if self.value == "ASSIGN":
            topmost_value = stack[-1]
            return stack[:-1], {**dictionary, **{self.variable_name: topmost_value}}
        if self.value == "RETRIEVE":
            return stack + [dictionary[self.variable_name]], dictionary
        else:
            raise NotImplementedError(f"Dictionary Operator {self.value} not implemented.")
