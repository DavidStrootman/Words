from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from src.interpreter.interpret_util import exhaustive_interpret_tokens


class ParserToken(ABC):
    """
    Base parser token.
    """

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Execute the token to get the result.
        :param stack: The stack to use fo2r executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        """
        raise RuntimeError(f"Tried to call unimplemented method \"execute\" on {self.__class__.__name__}.")


class DictionaryToken(ABC):
    """A visitable token that is stored in the dictionary."""

    class RemovedDictionaryToken:
        """Placeholder for tokens that are removed from the dictionary."""
        pass

    @abstractmethod
    def visit(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        The visit method is used to place a token on the dictionary, without executing it.

        :param stack: The stack used for visiting this token.
        :param dictionary: The dictionary used for visiting this token.
        :return: The stack and dictionary after this token has been visited..
        """
        pass


class NumberParserToken(ParserToken):
    """
    The number token represents an integer.
    """
    def __init__(self, value: int):
        self.value = value

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Execute the token to get the result.
        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        """
        return stack + [self.value], dictionary


class BooleanParserToken(ParserToken):
    """
    The boolean token represents a boolean.
    """
    def __init__(self, value: str):
        if value == "True":
            self.value = True
        if value == "False":
            self.value = False

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Execute the token to get the result.
        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        """
        return stack + [self.value], dictionary


class MacroParserToken(ParserToken):
    """
    The macro token represents a macro, for example __PRINT___.
    """
    def __init__(self, function_name: str):
        self.function_name = function_name

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Execute the token to get the result.
        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        """
        if self.function_name == "__PRINT__":
            print(stack[-1])
            return stack, dictionary


class WhileParserToken(ParserToken):
    """
    The while token represents a while loop. It holds a predicate that is checked every loop and the statements that
    should be executed as long as the predicate holds true.
    """
    def __init__(self, predicate: List[ParserToken], statements: List[ParserToken]):
        self.predicate = predicate
        self.statements = statements

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Execute the token to get the result.
        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        """
        predicate_outcome: bool = exhaustive_interpret_tokens(self.predicate, stack, dictionary)[0][0]
        if predicate_outcome:
            return self.execute(*exhaustive_interpret_tokens(self.statements, stack, dictionary))
        return stack, dictionary


class IfParserToken(ParserToken):
    """
    The if token represents an if statement, with an optional else statement.
    """
    def __init__(self, if_body: List[ParserToken], else_body: Optional[List[ParserToken]] = None):
        self.if_body = if_body
        self.else_body = else_body

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Execute the token to get the result.
        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        """
        predicate = stack[-1]
        if predicate is True:
            return exhaustive_interpret_tokens(self.if_body, stack[:-1], dictionary)
        if self.else_body:
            return exhaustive_interpret_tokens(self.else_body, stack[:-1], dictionary)
        return stack[:-1], dictionary


class VariableParserToken(ParserToken, DictionaryToken):
    """
    The variable token represents a variable. The variable token gets placed in the dictionary.
    """
    class VarUnassigned:
        pass

    def __init__(self, value: str):
        self.value: str = value
        self.assigned_value: any = self.VarUnassigned

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Execute the token to get the result.
        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        """
        if self.value in dictionary:
            raise KeyError(f"Variable {self.value} already exists in dictionary.")
        return stack, {**dictionary, **{self.value: self}}

    def visit(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        return stack + list([self.assigned_value]), dictionary


class ValueParserToken(ParserToken):
    """
    The value parser token represents a function parameter, which is called a value in Words.
    """
    def __init__(self, value: str):
        self.value = value

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Execute the token to get the result.
        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        """
        return stack + list([self.value]), dictionary


class IdentParserToken(ParserToken):
    """
    The identifier token represents an identifier.
    """
    def __init__(self, value: str):
        self.value = value

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Execute the token to get the result.
        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        """
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
    def __init__(self, name, parameters: List[ParserToken], body: List[ParserToken]):
        self.name = name
        if not all(isinstance(token, ValueParserToken) for token in parameters):
            raise RuntimeError(
                f"Got token that is not a ValueParserToken in Function Parameters in function {self.name}")
        self.parameters: List[ParserToken] = parameters
        self.body = body

    def execute(self, stack: list, dictionary: dict):
        """
        Execute the token to get the result.
        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        """
        if self.name in dictionary:
            raise KeyError(f"Function {self.name} already exists in dictionary.")
        dictionary[self.name] = self
        return stack, dictionary

    def visit(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        return stack[:-len(self.parameters)] + exhaustive_interpret_tokens(self.body, *self.setup_parameters(stack, dictionary.copy()))[
            0], dictionary

    def setup_parameters(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        def rec_setup_parameters(stack_: list, dictionary_: dict, parameters: list):
            if not parameters:
                return stack_, dictionary_

            return rec_setup_parameters(stack_[:-1], {**dictionary_, **{parameters[0].value: stack_[-1]}},
                                        parameters[1:])

        return rec_setup_parameters(stack, dictionary, self.parameters)


class ArithmeticOperatorParserToken(ParserToken):
    def __init__(self, value: str):
        self.value = value

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Execute the token to get the result.
        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        """
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
        """
        Execute the token to get the result.
        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        """
        if self.value == "==":
            topmost_value = stack[-1]
            second_value = stack[-2]
            return stack[:-2] + [second_value == topmost_value], dictionary
        if self.value == ">=":
            topmost_value = stack[-1]
            second_value = stack[-2]
            return stack[:-2] + [second_value >= topmost_value], dictionary
        if self.value == "<":
            topmost_value = stack[-1]
            second_value = stack[-2]
            return stack[:-2] + [second_value < topmost_value], dictionary
        raise NotImplementedError(f"Unimplemented BooleanOperator {self.value}")


class DictionaryOperatorParserToken(ParserToken):
    def __init__(self, value: str, variable_name: str):
        self.value = value
        self.variable_name = variable_name

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Execute the token to get the result.
        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        """
        if self.value == "ASSIGN":
            topmost_value = stack[-1]
            return stack[:-1], {**dictionary, **{self.variable_name: topmost_value}}
        if self.value == "RETRIEVE":
            return stack + [dictionary[self.variable_name]], dictionary
        else:
            raise NotImplementedError(f"Dictionary Operator {self.value} not implemented.")
