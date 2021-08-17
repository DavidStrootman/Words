import random
from typing import Iterator, List, Tuple, Dict

import pytest

from words.exceptions.parser_exceptions import StackSizeException, InvalidPredicateException
from words.lexer.lex import Lexer
from words.lexer.lex_util import DebugData
from words.parser.parse import Parser
from words.token_types.lexer_token import LexerToken
from words.token_types.parser_token import NumberParserToken, BooleanParserToken, MacroParserToken, ParserToken, \
    WhileParserToken, IfParserToken
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
        token = NumberParserToken(DebugData(0), random_int)
        assert token.execute([], {}) == ([random_int], {})

    def test_execute_return_value(self):
        """Test a return value is given."""
        token = NumberParserToken(DebugData(0), 16)
        assert token.execute([], {}) != ([], {})


class TestBooleanParserToken:
    def test_init_value(self):
        token = BooleanParserToken(DebugData(0), "True")
        assert isinstance(token.value, bool)
        token = BooleanParserToken(DebugData(0), "False")
        assert isinstance(token.value, bool)

    def test_execute_positive(self):
        """Test the return value is correct for a boolean token."""
        token_true = BooleanParserToken(DebugData(0), "True")
        assert token_true.execute([], {}) == ([True], {})

        token_false = BooleanParserToken(DebugData(0), "False")
        assert token_false.execute([], {}) == ([False], {})

    def test_execute_return_value(self):
        """Test a return value is given."""
        token = BooleanParserToken(DebugData(0), "True")
        assert token.execute([], {}) != ([], {})
        token = BooleanParserToken(DebugData(0), "False")
        assert token.execute([], {}) != ([], {})


class TestMacroParserToken:
    def test_execute_print_positive(self, capsys):
        """The print macro should output the topmost value to stdout."""
        token = MacroParserToken(DebugData(0), "__PRINT__")
        number_to_print = 42

        token.execute([number_to_print], {})

        captured_print = capsys.readouterr()
        assert captured_print.out == f"{number_to_print}\n"

    def test_execute_print_invalid_stack_size(self):
        """An exception should be raised if the code tried to print from an empty stack."""
        token = MacroParserToken(DebugData(0), "__PRINT__")

        with pytest.raises(StackSizeException):
            token.execute([], {})

    def test_execute_print_output(self):
        """Make sure the stack and dictionary are returned after printing."""
        token = MacroParserToken(DebugData(0), "__PRINT__")
        number_to_print = 42

        assert token.execute([number_to_print], {}) == ([number_to_print], {})


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
        token = WhileParserToken(DebugData(0), predicate, body)
        result = token.execute(*initial_state)
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
        token = WhileParserToken(DebugData(0), predicate, body)
        with pytest.raises(InvalidPredicateException):
            token.execute([], {})

    def test_execute_false_predicate(self):
        """The while body should not run if the predicate is never true."""
        token = WhileParserToken(DebugData(0), _parse_from_string("False"), _parse_from_string("0"))
        assert not token.execute([], {})[0]


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
        token = IfParserToken(DebugData(0), if_body)
        assert token.execute(*condition)[0][0] == 3

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
        token = IfParserToken(DebugData(0), if_body)
        assert not token.execute(*condition)[0]

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
        token = IfParserToken(DebugData(0), if_body, else_body)
        assert token.execute(*condition)[0][0] == 13

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
        token = IfParserToken(DebugData(0), if_body, else_body)
        with pytest.raises(InvalidPredicateException):
            token.execute(*condition)
