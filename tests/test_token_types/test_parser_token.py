import random
from typing import Iterator, List, Tuple, Dict

import pytest

from words.exceptions.parser_exceptions import StackSizeException, InvalidPredicateException, \
    UndefinedIdentifierException, IdentifierPreviouslyDefinedException
from words.lexer.lex import Lexer
from words.lexer.lex_util import DebugData
from words.parser.parse import Parser
from words.token_types.lexer_token import LexerToken
from words.token_types.parser_token import NumberParserToken, BooleanParserToken, MacroParserToken, ParserToken, \
    WhileParserToken, IfParserToken, ValueParserToken, IdentParserToken, VariableParserToken, ReturnParserToken, \
    FunctionParserToken, LambdaParserToken, ArithmeticOperatorParserToken, BooleanOperatorParserToken, \
    DictionaryOperatorParserToken
from words.interpreter.interpret_util import exhaustive_interpret_tokens


def _parse_from_string(words: str) -> List[ParserToken]:
    contents_with_line_nums = enumerate(iter(words.splitlines()))
    lexed_tokens: Iterator[LexerToken] = Lexer.lex_file_contents(contents_with_line_nums)
    return Parser.parse(lexed_tokens).tokens


def _execute_from_string(words: str) -> Tuple[List[ParserToken], Dict[str, ParserToken]]:
    contents_with_line_nums = enumerate(iter(words.splitlines()))
    lexed_tokens: Iterator[LexerToken] = Lexer.lex_file_contents(contents_with_line_nums)
    return exhaustive_interpret_tokens(Parser.parse(lexed_tokens).tokens, [], {})


class TestParserToken:
    """Test base class functionality with a concrete implementation."""

    def test_debug_str(self):
        class ConcreteParserToken(ParserToken):
            def execute(self, stack: list, dictionary: dict) -> Tuple[list, dict]:
                """Abstract method does not need to be tested"""

        assert isinstance(ConcreteParserToken(DebugData(0)).debug_str(), str)


class TestDictionaryToken:
    """No functionality in base class to test."""


class TestNumberParserToken:
    def test_execute_positive(self):
        """Test the return value is correct for a number token."""
        random_int = random.randint(0, 100)
        number_token = NumberParserToken(DebugData(0), random_int)
        assert number_token.execute([], {}) == ([random_int], {})

    def test_execute_return_value(self):
        """Test a return value is given."""
        number_token = NumberParserToken(DebugData(0), 16)
        assert number_token.execute([], {}) != ([], {})


class TestBooleanParserToken:
    def test_init_value(self):
        bool_token = BooleanParserToken(DebugData(0), "True")
        assert isinstance(bool_token.value, bool)
        bool_token = BooleanParserToken(DebugData(0), "False")
        assert isinstance(bool_token.value, bool)

    def test_execute_positive(self):
        """Test the return value is correct for a boolean token."""
        bool_token_true = BooleanParserToken(DebugData(0), "True")
        assert bool_token_true.execute([], {}) == ([True], {})

        bool_token_false = BooleanParserToken(DebugData(0), "False")
        assert bool_token_false.execute([], {}) == ([False], {})

    def test_execute_return_value(self):
        """Test a return value is given."""
        bool_token = BooleanParserToken(DebugData(0), "True")
        assert bool_token.execute([], {}) != ([], {})
        bool_token = BooleanParserToken(DebugData(0), "False")
        assert bool_token.execute([], {}) != ([], {})


class TestMacroParserToken:
    def test_execute_print_positive(self, capsys):
        """The print macro should output the topmost value to stdout."""
        macro = MacroParserToken(DebugData(0), "__PRINT__")
        number_to_print = 42

        macro.execute([number_to_print], {})

        captured_print = capsys.readouterr()
        assert captured_print.out == f"{number_to_print}\n"

    def test_execute_print_invalid_stack_size(self):
        """An exception should be raised if the code tried to print from an empty stack."""
        macro = MacroParserToken(DebugData(0), "__PRINT__")

        with pytest.raises(StackSizeException):
            macro.execute([], {})

    def test_execute_print_output(self):
        """Make sure the stack and dictionary are returned after printing."""
        macro = MacroParserToken(DebugData(0), "__PRINT__")
        number_to_print = 42

        assert macro.execute([number_to_print], {}) == ([number_to_print], {})


class TestWhileParserToken:
    def test_execute_positive(self):
        """Test a valid while loop configuration."""
        # Fixture
        initial_state: Tuple[List, Dict] = _execute_from_string(
            "VARIABLE SOME_VAR "
            "0 ASSIGN SOME_VAR"
        )

        predicate: List[ParserToken] = _parse_from_string(
            "SOME_VAR 10 < "
        )

        body: List[ParserToken] = _parse_from_string(
            "SOME_VAR 1 + "
            "ASSIGN SOME_VAR"
        )

        # Test
        while_statement = WhileParserToken(DebugData(0), predicate, body)
        result = while_statement.execute(*initial_state)
        assert result[1]['SOME_VAR'] == 10

    def test_execute_non_bool_predicate(self):
        """A while loop requires a valid (boolean) predicate."""
        # Fixture
        predicate: List[ParserToken] = _parse_from_string(
            "10"
        )
        body: List[ParserToken] = _parse_from_string(
            "203"
        )

        # Test
        while_statement = WhileParserToken(DebugData(0), predicate, body)
        with pytest.raises(InvalidPredicateException):
            while_statement.execute([], {})

    def test_execute_false_predicate(self):
        """The while body should not run if the predicate is never true."""
        while_statement = WhileParserToken(DebugData(0), _parse_from_string("False"), _parse_from_string("0"))
        assert not while_statement.execute([], {})[0]


class TestIfParserToken:
    def test_execute_true_condition(self):
        """Test a correct if statement with a body and an else body."""
        # Fixture
        condition = _execute_from_string(
            "True"
        )
        if_body = _parse_from_string(
            "3"
        )
        # Assert stack equals the value in if body
        if_statement = IfParserToken(DebugData(0), if_body)
        assert if_statement.execute(*condition)[0][0] == 3

    def test_execute_false_condition(self):
        """If the condition is false, the if token should execute the else body."""
        # Fixture
        condition = _execute_from_string(
            "False"
        )
        if_body = _parse_from_string(
            "7"
        )

        # Assert stack is empty, so if body is not executed
        if_statement = IfParserToken(DebugData(0), if_body)
        assert not if_statement.execute(*condition)[0]

    def test_execute_false_condition_else(self):
        """If the condition is false, the if token should execute the else body."""
        # Fixture
        condition = _execute_from_string(
            "False"
        )
        if_body = _parse_from_string(
            "7"
        )
        else_body = _parse_from_string(
            "13"
        )

        # Assert stack equals the value in else body
        if_statement = IfParserToken(DebugData(0), if_body, else_body)
        assert if_statement.execute(*condition)[0][0] == 13

    def test_execute_non_bool_predicate(self):
        """The if statement requires a boolean condition value before executing."""
        # Fixture
        condition = _execute_from_string(
            "0"
        )
        if_body = _parse_from_string(
            "9"
        )
        else_body = _parse_from_string(
            "2"
        )

        # Assert an invalid predicate exception is raised if the condition is not a boolean value
        if_statement = IfParserToken(DebugData(0), if_body, else_body)
        with pytest.raises(InvalidPredicateException):
            if_statement.execute(*condition)


class TestVariableParserToken:
    def test_execute_positive(self):
        """Test creating a variable in the dictionary."""
        variable = VariableParserToken(DebugData(0), "SOME_VAR")
        result = variable.execute([], {})
        assert "SOME_VAR" in result[1]

    def test_execute_duplicate_definition(self):
        """
        If a variable is defined that already exists an
         exception should be raised, since shadowing is not allowed
        """
        variable_definition = _execute_from_string(
            "VARIABLE DEFINED_VAR"
        )
        variable = VariableParserToken(DebugData(0), "DEFINED_VAR")
        with pytest.raises(IdentifierPreviouslyDefinedException):
            variable.execute(*variable_definition)

    def test_visit_positive(self):
        """Test visiting a variable returns its value on the stack."""
        variable = VariableParserToken(DebugData(0), "VAR")
        variable.assigned_value = 62
        assert variable.visit([12], {})[0] == [12, 62]


class TestValueParserToken:
    def test_execute(self):
        """Values cannot be executed, only added to the dictionary when instantiating a function."""
        with pytest.raises(RuntimeError):
            ValueParserToken(DebugData(0), "SOME_VALUE").execute([], {})


class TestIdentParserToken:
    def test_execute_negative(self):
        """If a key that is not in the dictionary is provided, an undefined variable exception should be raised."""
        # Fixture
        var_decl = _execute_from_string(
            "VARIABLE A"
        )

        # Assert the token value is retrieved if it exists in the dictionary
        identifier = IdentParserToken(DebugData(0), "B")
        with pytest.raises(UndefinedIdentifierException):
            assert identifier.execute(*var_decl)[0][0] == VariableParserToken.VarUnassigned

    def test_execute_variable(self):
        """If the variable identifier key is found in the dictionary, its value should be returned."""
        # Fixture
        var_decl = _execute_from_string(
            "VARIABLE X"
        )

        # Assert the token value is retrieved if it exists in the dictionary
        identifier = IdentParserToken(DebugData(0), "X")
        assert identifier.execute(*var_decl)[0][0] == VariableParserToken.VarUnassigned

    def test_execute_function(self):
        """If the function identifier key is found in the dictionary, it should be executed."""
        # Fixture
        func_decl = _execute_from_string(
            "| SOME_FUNC ( ) "
            "8 12 81751692 "
            "RETURN 3 |"
        )
        # Assert the function is executed and its return value is retrieved
        identifier = IdentParserToken(DebugData(0), "SOME_FUNC")
        result = identifier.execute(*func_decl)
        assert result[0] == [8, 12, 81751692]


class TestReturnParserToken:
    def test_execute_positive(self):
        """Test the correct amount of values are returned onto the stack."""
        # Fixture
        values_on_stack_in_function = _execute_from_string(
            "1512 125 92"
        )
        # Assert all values are on the new stack after returning them
        return_token = ReturnParserToken(DebugData(0), 3)
        result = return_token.execute(*values_on_stack_in_function)
        assert result[0] == [1512, 125, 92]

    def test_execute_return_not_all_values(self):
        """If the return count is smaller than the local stack, only count values should be returned."""
        # Fixture
        values_on_stack_in_function = _execute_from_string(
            "92 82928 9282 923839 162"
        )
        # Assert only the last two values are returned from the stack
        return_token = ReturnParserToken(DebugData(0), 2)
        result = return_token.execute(*values_on_stack_in_function)
        assert result[0] == [923839, 162]

    def test_execute_not_enough_values_on_stack(self):
        """If fewer values exist on the stack than the return expects, an exception should be raised."""
        # Fixture
        values_on_stack_in_function = _execute_from_string(
            "92 92"
        )
        # Assert an exception is raised, since not enough values are on the stack
        return_token = ReturnParserToken(DebugData(0), 3)
        with pytest.raises(StackSizeException):
            return_token.execute(*values_on_stack_in_function)

    def test_execute_zero_count(self):
        """
        If the return count is zero, no value should be returned,
         this is equivalent to having no RETURN statement.
        """
        # Fixture
        values_on_stack_in_funcion = _execute_from_string(
            "9829 929"
        )
        # Assert no value is returned
        return_token = ReturnParserToken(DebugData(0), 0)
        result = return_token.execute(*values_on_stack_in_funcion)
        assert not result[0]


class TestFunctionParserToken:
    def test_execute_positive(self):
        """Test placing a function in the dictionary that does not yet exist."""
        function_decl = FunctionParserToken(DebugData(0), "SOME_FUNC", [], [])
        result = function_decl.execute([], {})
        assert "SOME_FUNC" in result[1]

    def test_execute_duplicate_definition(self):
        """If the function was already defined, it cannot be defined again."""
        # Fixture
        initial_state = _execute_from_string(
            "| DEFINED_FUNC ( ) |"
        )
        # Assert an exception is raised if the function was previously defined
        function_decl = FunctionParserToken(DebugData(0), "DEFINED_FUNC", [], [])
        with pytest.raises(IdentifierPreviouslyDefinedException):
            function_decl.execute(*initial_state)

    def test_visit_positive(self):
        """Test executing the function body."""
        # Fixture
        function_with_body = _parse_from_string(
            "| FNC_BODY ( ) 1 2 3 RETURN 3 |"
        )[0]
        # Assert the parsed string returns a function
        assert isinstance(function_with_body, FunctionParserToken)
        # Assert the visit function executes the body correctly.
        assert function_with_body.visit([], {})[0] == [1, 2, 3]

    def test_visit_setup_parameters(self):
        """The parameters should be accessible during visit."""
        # Fixture
        function_with_params = _parse_from_string(
            "| FNC_PARAM ( VALUE X ) X RETURN 1 |"
        )[0]
        # Assert the parsed string returns a function
        assert isinstance(function_with_params, FunctionParserToken)
        # Assert the visit function accepts the parameter and returns it
        assert function_with_params.visit([20], {})[0] == [20]

    def test_visit_parameters_eaten_from_stack(self):
        """Assert all parameters taken are removed from the stack."""
        # Fixture
        function = _parse_from_string(
            "| FNC ( VALUE X VALUE Y VALUE Z ) |"
        )[0]
        # Assert the parsed string returns a function
        assert isinstance(function, FunctionParserToken)
        # Assert the visit function accepts the parameter and returns it
        assert function.visit([1, 2, 3, 4], {})[0] == [1]

    def test_setup_parameters_positive(self):
        """Assert parameters are setup correctly."""
        # Fixture
        function = _parse_from_string(
            "| FNC ( VALUE X VALUE Y ) |"
        )[0]
        # Assert the parsed string returns a function
        assert isinstance(function, FunctionParserToken)
        # Assert the visit function accepts the parameter and returns it
        assert function.setup_parameters([37, 62], {})[1] == {"Y": 37, "X": 62}

    def test_setup_parameters_invalid_stack_size(self):
        """If the stack is not large enough to set up parameters an exception should be raised."""
        # Fixture
        function = _parse_from_string(
            "| FNC ( VALUE X VALUE Y ) |"
        )[0]
        # Assert the parsed string returns a function
        assert isinstance(function, FunctionParserToken)
        # Assert an exception is raised, since only one of the two parameters can be set up
        with pytest.raises(StackSizeException):
            function.setup_parameters([37], {})


@pytest.mark.xfail(reason="Lambdas are not implemented.")
class TestLambdaParserToken:
    def test_execute_positive(self):
        token = LambdaParserToken(DebugData(0))
        token.execute([], {})


class TestArithmeticOperatorParserToken:
    def test_execute_addition(self):
        addition_operator = ArithmeticOperatorParserToken(DebugData(0), "+")
        result = addition_operator.execute([25, 52], {})
        assert result[0] == [25 + 52]

    def test_execute_subtraction(self):
        subtraction_operator = ArithmeticOperatorParserToken(DebugData(0), "-")
        result = subtraction_operator.execute([25, 52], {})
        assert result[0] == [25 - 52]

    def test_execute_unimplemented_operator(self):
        operator = ArithmeticOperatorParserToken(DebugData(0), "SOME_UNIMPLEMENTED_OP")
        with pytest.raises(NotImplementedError):
            operator.execute([643, 72], {})

    def test_execute_invalid_stack_size(self):
        """An arithmetic operator expects at least two values on the stack."""
        operator = ArithmeticOperatorParserToken(DebugData(0), "+")
        with pytest.raises(StackSizeException):
            operator.execute([25], {})


class TestBooleanOperatorParserToken:
    def test_execute_equality(self):
        operator = BooleanOperatorParserToken(DebugData(0), "==")
        result = operator.execute([52, 52], {})
        assert result[0] == [True]
        operator = BooleanOperatorParserToken(DebugData(0), "==")
        result = operator.execute([52, 85], {})
        assert result[0] == [False]

    def test_execute_greater(self):
        operator = BooleanOperatorParserToken(DebugData(0), ">")
        result = operator.execute([52, 27], {})
        assert result[0] == [True]
        operator = BooleanOperatorParserToken(DebugData(0), ">")
        result = operator.execute([52, 85], {})
        assert result[0] == [False]
        operator = BooleanOperatorParserToken(DebugData(0), ">")
        result = operator.execute([52, 52], {})
        assert result[0] == [False]

    def test_execute_lesser(self):
        operator = BooleanOperatorParserToken(DebugData(0), "<")
        result = operator.execute([64, 108], {})
        assert result[0] == [True]
        operator = BooleanOperatorParserToken(DebugData(0), "<")
        result = operator.execute([872, 87], {})
        assert result[0] == [False]
        operator = BooleanOperatorParserToken(DebugData(0), "<")
        result = operator.execute([64, 64], {})
        assert result[0] == [False]

    def test_execute_greater_eq(self):
        operator = BooleanOperatorParserToken(DebugData(0), ">=")
        result = operator.execute([1252, 87], {})
        assert result[0] == [True]
        operator = BooleanOperatorParserToken(DebugData(0), ">=")
        result = operator.execute([728, 27822], {})
        assert result[0] == [False]
        operator = BooleanOperatorParserToken(DebugData(0), ">=")
        result = operator.execute([252, 252], {})
        assert result[0] == [True]

    def test_execute_lesser_eq(self):
        operator = BooleanOperatorParserToken(DebugData(0), "<=")
        result = operator.execute([728, 2758], {})
        assert result[0] == [True]
        operator = BooleanOperatorParserToken(DebugData(0), "<=")
        result = operator.execute([5172, 1272], {})
        assert result[0] == [False]
        operator = BooleanOperatorParserToken(DebugData(0), "<=")
        result = operator.execute([2782, 2782], {})
        assert result[0] == [True]

    def test_execute_invalid_stack_size(self):
        """A boolean operator expects at least two values on the stack."""
        operator = BooleanOperatorParserToken(DebugData(0), "==")
        with pytest.raises(StackSizeException):
            operator.execute([9262], {})

    def test_execute_unimplemented_operator(self):
        operator = BooleanOperatorParserToken(DebugData(0), "SOME_UNIMPLEMENTED_OP")
        with pytest.raises(NotImplementedError):
            operator.execute([825, 92], {})


class TestDictionaryOperatorParserToken:
    def test_execute_assign(self):
        operator = DictionaryOperatorParserToken(DebugData(0), "ASSIGN", "X")
        result = operator.execute([28], {"X": VariableParserToken.VarUnassigned})
        # Assert the value is removed from the stack
        assert not result[0]
        # Assert the value from the stack is assigned to the variable
        assert result[1]["X"] == 28

    def test_execute_retrieve(self):
        operator = DictionaryOperatorParserToken(DebugData(0), "RETRIEVE", "X")
        result = operator.execute([], {"X": 82})
        # Assert the value of the variable is placed on the stack
        assert result[0] == [82]

    def test_execute_assign_invalid_stack_size(self):
        """A dictionary operator expects at least one value on the stack."""
        operator = DictionaryOperatorParserToken(DebugData(0), "ASSIGN", "SOME_VAR")
        with pytest.raises(StackSizeException):
            operator.execute([], {})

    def test_execute_unimplemented_operator(self):
        operator = DictionaryOperatorParserToken(DebugData(0), "SOME_UNIMPLEMENTED_OP", "SOME_OTHER_VAR")
        with pytest.raises(NotImplementedError):
            operator.execute([23], {})
