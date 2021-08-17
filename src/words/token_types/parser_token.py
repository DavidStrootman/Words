from abc import abstractmethod
from typing import List, Optional, Tuple

from words.exceptions.parser_exceptions import StackSizeException, InvalidPredicateException
from words.helper.Debuggable import Debuggable
from words.helper.PrintableABC import PrintableABC
from words.interpreter.interpret_util import exhaustive_interpret_tokens
from words.lexer.lex_util import DebugData


class ParserToken(Debuggable, PrintableABC):
    """
    Base parser token.
    """
    def __init__(self, debug_data: DebugData):
        self.debug_data = debug_data

    @abstractmethod
    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Execute the token to get the result.
        :param stack: The stack to use fo2r executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        """

    def debug_str(self):
        return f"\"{self}\" at line {self.debug_data}"


class DictionaryToken:
    """A visitable token that is stored in the dictionary."""

    class RemovedDictionaryToken:
        """Placeholder for tokens that are removed from the dictionary."""

    @abstractmethod
    def visit(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        The visit method is used to place a token on the dictionary, without executing it.

        :param stack: The stack used for visiting this token.
        :param dictionary: The dictionary used for visiting this token.
        :return: The stack and dictionary after this token has been visited..
        """


class NumberParserToken(ParserToken):
    """
    The number token represents an integer.
    """
    def __init__(self, debug_data: DebugData, value: int):
        super().__init__(debug_data)
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
    def __init__(self, debug_data: DebugData, value: str):
        super().__init__(debug_data)

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
    def __init__(self, debug_data: DebugData, function_name: str):
        super().__init__(debug_data)

        self.function_name = function_name

    def debug_str(self):
        return f"\"{self.function_name}\" at line {self.debug_data}"

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Execute the token to get the result.
        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        """
        if self.function_name == "__PRINT__":
            if not stack:
                raise StackSizeException(token=self, expected_size=1, actual_size=0)
            print(stack[-1])
            return stack, dictionary


class WhileParserToken(ParserToken):
    """
    The while token represents a while loop. It holds a predicate that is checked every loop and the statements that
    should be executed as long as the predicate holds true.
    """
    def __init__(self, debug_data: DebugData, predicate: List[ParserToken], statements: List[ParserToken]):
        super().__init__(debug_data)

        self.predicate: List[ParserToken] = predicate
        self.statements: List[ParserToken] = statements

    def debug_str(self):
        return f"\"WHILE\" token at line {self.debug_data.line + 1}"

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Execute the token to get the result.
        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        """
        predicate_outcome: bool = exhaustive_interpret_tokens(self.predicate, stack, dictionary)[0][0]
        if not isinstance(predicate_outcome, bool):
            raise InvalidPredicateException(self)
        if predicate_outcome:
            return self.execute(*exhaustive_interpret_tokens(self.statements, stack, dictionary))
        return stack, dictionary


class IfParserToken(ParserToken):
    """
    The if token represents an if statement, with an optional else statement.
    """
    def __init__(self, debug_data: DebugData,
                 if_body: List[ParserToken],
                 else_body: Optional[List[ParserToken]] = None):
        super().__init__(debug_data)

        self.if_body: List[ParserToken] = if_body
        self.else_body: Optional[List[ParserToken]] = else_body

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

    def __init__(self, debug_data: DebugData, value: str):
        super().__init__(debug_data)

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
        return stack, {**dictionary, **{self.value: self.assigned_value}}

    def visit(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        return stack + list([self.assigned_value]), dictionary


class ValueParserToken(ParserToken):
    """
    The value parser token represents a function parameter, which is called a value in Words.
    """
    def __init__(self, debug_data: DebugData, value: str):
        super().__init__(debug_data)

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
    def __init__(self, debug_data: DebugData, value: str):
        super().__init__(debug_data)

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
    def __init__(self, debug_data: DebugData, count: int):
        super().__init__(debug_data)

        self.count = count

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        if len(stack) < self.count:
            raise StackSizeException(token=self, expected_size=self.count, actual_size=len(stack))
        if self.count == 0:
            return [], dictionary
        return stack[-self.count:], dictionary

    def debug_str(self):
        return f"\"RETURN\" at line {self.debug_data}"


class FunctionParserToken(ParserToken, DictionaryToken):
    def __init__(self, debug_data: DebugData, name, parameters: List[ParserToken], body: List[ParserToken]):
        super().__init__(debug_data)

        self.name = name
        if not all(isinstance(token, ValueParserToken) for token in parameters):
            raise RuntimeError(
                f"Got token that is not a ValueParserToken in Function Parameters in function {self.name}")
        self.parameters: List[ParserToken] = parameters
        self.body = body

    def execute(self, stack: list, dictionary: dict):
        """
        Setup the function by placing it in the dictionary.
        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        """
        if self.name in dictionary:
            raise KeyError(f"Function {self.name} already exists in dictionary.")
        dictionary[self.name] = self
        return stack, dictionary

    def visit(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Execute the function body and get the result.
        :param stack:
        :param dictionary:
        :return:
        """
        parameters = self.setup_parameters(stack, dictionary.copy())
        new_stack = stack[:-len(self.parameters)] + exhaustive_interpret_tokens(self.body, *parameters)[0]
        return new_stack, dictionary

    def setup_parameters(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        def rec_setup_parameters(stack_: list, dictionary_: dict, parameters: list):
            if not parameters:
                return stack_, dictionary_
            if len(stack) < len(self.parameters):
                raise StackSizeException(token=self, expected_size=len(self.parameters), actual_size=len(stack))

            return rec_setup_parameters(stack_[:-1], {**dictionary_, **{parameters[0].value: stack_[-1]}},
                                        parameters[1:])

        return rec_setup_parameters(stack, dictionary, self.parameters)

    def debug_str(self):
        return f"function \"{self.name}\" at line {self.debug_data}"


class LambdaParserToken(ParserToken):
    """TODO: Lambdas."""

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        raise NotImplementedError("Lambdas not implemented yet.")


class ArithmeticOperatorParserToken(ParserToken):
    def __init__(self, debug_data: DebugData, value: str):
        super().__init__(debug_data)

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
        raise NotImplementedError(f"Unimplemented ArithmeticOperator {self.value}")


class BooleanOperatorParserToken(ParserToken):
    def __init__(self, debug_data: DebugData, value: str):
        super().__init__(debug_data)

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
    def __init__(self, debug_data: DebugData, value: str, variable_name: str):
        super().__init__(debug_data)

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
