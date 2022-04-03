from abc import abstractmethod
from typing import List, Optional, Tuple

from words.exceptions.parser_exceptions import StackSizeException, InvalidPredicateException, \
    UndefinedIdentifierException, IdentifierPreviouslyDefinedException
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

        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        """

    def debug_str(self) -> str:
        """A debug string is used for providing better error messages during both parsing and at runtime."""
        return f"\"{self}\" at line {self.debug_data}"


class DictionaryToken:
    """A visitable token that is stored in the dictionary."""

    class RemovedDictionaryToken:
        """Placeholder for tokens that are removed from the dictionary."""

    @abstractmethod
    def visit(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        The visit method is used for tokens that might have some other use after the initial execute. For example the
        function parser token is placed in the dictionary during execution, and run during visiting.

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
        Executing a number parser token places its value on the stack.

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
        Executing a boolean parser token places its value on the stack.

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

    def debug_str(self) -> str:
        """A debug string is used for providing better error messages during both parsing and at runtime."""
        return f"\"{self.function_name}\" at line {self.debug_data}"

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Execute the macro.

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

    def debug_str(self) -> str:
        """A debug string is used for providing better error messages during both parsing and at runtime."""
        return f"\"WHILE\" token at line {self.debug_data}"

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Run the while loop as long as the predicate holds true.

        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        :raises InvalidPredicateException: If the predicate does not return a boolean value the while loop cannot know
         if it should run.
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

    def debug_str(self) -> str:
        """A debug string is used for providing better error messages during both parsing and at runtime."""
        return f"\"IF\" token at line {self.debug_data}"

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Either run the if or else body, based on the predicate.

        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        :raises InvalidPredicateException: If the predicate does not return a boolean value the if statement cannot know
         if it should run.
        """
        predicate = stack[-1]
        if not isinstance(predicate, bool):
            raise InvalidPredicateException(self)
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

    def debug_str(self) -> str:
        """A debug string is used for providing better error messages during both parsing and at runtime."""
        return f"variable with name \"{self.value}\" at line {self.debug_data}"

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Execute the variable to place it in the dictionary, with Unassigned as its value.

        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        :raises IdentifierPreviouslyDefinedException: Since shadowing is not allowed, a variable cannot be defined
         twice.
        """
        if self.value in dictionary:
            raise IdentifierPreviouslyDefinedException(self)
        return stack, {**dictionary, **{self.value: self.assigned_value}}

    def visit(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Visiting a variable retrieves its assigned value and places it on the stack.
        :param stack:
        :param dictionary:
        :return:
        """
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
        Values cannot be executed, only added to the dictionary when instantiating a function.

        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        """
        raise RuntimeError("Value parser tokens cannot be executed, but must instead be"
                           " added to the dictionary by the function.")


class IdentParserToken(ParserToken):
    """
    The identifier parser token represents an identifier.
    """

    def __init__(self, debug_data: DebugData, value: str):
        super().__init__(debug_data)

        self.value = value

    def debug_str(self) -> str:
        """A debug string is used for providing better error messages during both parsing and at runtime."""
        return f"identifier \"{self.value}\" at line {self.debug_data}"

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
        raise UndefinedIdentifierException(self)


class ReturnParserToken(ParserToken):
    def __init__(self, debug_data: DebugData, count: int):
        super().__init__(debug_data)

        self.count = count

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """

        :param stack:
        :param dictionary:
        :return:
        """
        if len(stack) < self.count:
            raise StackSizeException(token=self, expected_size=self.count, actual_size=len(stack))
        if self.count == 0:
            return [], dictionary
        return stack[-self.count:], dictionary

    def debug_str(self) -> str:
        """A debug string is used for providing better error messages during both parsing and at runtime."""
        return f"\"RETURN\" at line {self.debug_data}"


class FunctionParserToken(ParserToken, DictionaryToken):
    """
    A function parser token represents a function. It can be executed to place it in the dictionary and visited to run
     the statements in the body of the function.
    """
    def __init__(self, debug_data: DebugData, name: str, parameters: List[ParserToken], body: List[ParserToken]):
        super().__init__(debug_data)

        self.name: str = name
        self.parameters: List[ParserToken] = parameters
        self.body: List[ParserToken] = body

    def execute(self, stack: list, dictionary: dict):
        """
        Setup the function by placing it in the dictionary.

        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        """
        if self.name in dictionary:
            raise IdentifierPreviouslyDefinedException(self)
        dictionary[self.name] = self
        return stack, dictionary

    def visit(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Set up the parameters and execute the function body.

        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        """
        stripped_stack, parameters = self.setup_parameters(stack, dictionary.copy())
        new_stack = stripped_stack + exhaustive_interpret_tokens(self.body, stripped_stack, parameters)[0]
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

    def debug_str(self) -> str:
        """A debug string is used for providing better error messages during both parsing and at runtime."""
        return f"function \"{self.name}\" at line {self.debug_data}"


class LambdaParserToken(ParserToken):
    """TODO: Lambdas."""

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        raise NotImplementedError("Lambdas not implemented yet.")


class ArithmeticOperatorParserToken(ParserToken):
    """
    An arithmetic operator parser token represents an arithmetic operation. For example the addition operation. It holds
    both the type of operation, as well as the values it will operate on.
    """
    def __init__(self, debug_data: DebugData, value: str):
        super().__init__(debug_data)
        self.value = value

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Execute the arithmetic operation.

        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        :raises StackSizeException: An arithmetic operator always needs two values to run.
        :raises NotImplementedError: If an undefined operator is specified it cannot run.
        """
        if len(stack) < 2:
            raise StackSizeException(self, 2, len(stack))
        topmost_value = stack[-1]
        second_value = stack[-2]

        if self.value == "+":
            return stack[:-2] + [second_value + topmost_value], dictionary
        if self.value == "-":
            return stack[:-2] + [second_value - topmost_value], dictionary
        raise NotImplementedError(f"Unimplemented ArithmeticOperator {self.value}")


class BooleanOperatorParserToken(ParserToken):
    """
    An boolean operator parser token represents a boolean operation. For example the equality operation. It holds
    both the type of operation, as well as the values it will operate on.
    """
    def __init__(self, debug_data: DebugData, value: str):
        super().__init__(debug_data)

        self.value = value

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Execute the boolean operation.

        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        :raises StackSizeException: A boolean operation always needs two values to run.
        :raises NotImplementedError: If an undefined operator is specified it cannot run.
        """
        if len(stack) < 2:
            raise StackSizeException(self, 2, len(stack))

        if self.value == "==":
            topmost_value = stack[-1]
            second_value = stack[-2]
            return stack[:-2] + [second_value == topmost_value], dictionary
        if self.value == ">":
            topmost_value = stack[-1]
            second_value = stack[-2]
            return stack[:-2] + [second_value > topmost_value], dictionary
        if self.value == "<":
            topmost_value = stack[-1]
            second_value = stack[-2]
            return stack[:-2] + [second_value < topmost_value], dictionary
        if self.value == ">=":
            topmost_value = stack[-1]
            second_value = stack[-2]
            return stack[:-2] + [second_value >= topmost_value], dictionary
        if self.value == "<=":
            topmost_value = stack[-1]
            second_value = stack[-2]
            return stack[:-2] + [second_value <= topmost_value], dictionary

        raise NotImplementedError(f"Unimplemented BooleanOperator {self.value}")


class DictionaryOperatorParserToken(ParserToken):
    """
    A dictionary operator parser token represents a dictionary operation. Dictionary operators are used for interacting
    with the dictionary. For example the assign operator assigns the top value from the stack to the provided
    identifier in the dictionary.
    """
    def __init__(self, debug_data: DebugData, value: str, variable_name: str):
        super().__init__(debug_data)

        self.value = value
        self.variable_name = variable_name

    def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
        """
        Execute the dictionary operation.

        :param stack: The stack to use for executing the token.
        :param dictionary: The dictionary to use for executing the token.
        :return: The stack and dictionary after executing the token.
        :raises NotImplementedError: If an undefined operator is specified it cannot run.
        """

        if self.value == "ASSIGN":
            if len(stack) < 1:
                raise StackSizeException(self, 1, len(stack))

            topmost_value = stack[-1]
            return stack[:-1], {**dictionary, **{self.variable_name: topmost_value}}
        else:
            raise NotImplementedError(f"Dictionary Operator {self.value} not implemented.")
