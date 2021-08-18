import random
from typing import Iterator, List, Tuple, Dict

import pytest

from words.exceptions.parser_exceptions import StackSizeException, InvalidPredicateException, \
    UndefinedIdentifierException
from words.lexer.lex import Lexer
from words.lexer.lex_util import DebugData
from words.parser.parse import Parser
from words.token_types.lexer_token import LexerToken
from words.token_types.parser_token import NumberParserToken, BooleanParserToken, MacroParserToken, ParserToken, \
    WhileParserToken, IfParserToken, ValueParserToken, IdentParserToken, VariableParserToken
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
