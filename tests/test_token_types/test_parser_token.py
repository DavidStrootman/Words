import random

import pytest

from words.exceptions.parser_exceptions import StackSizeException
from words.lexer.lex_util import DebugData
from words.token_types.parser_token import NumberParserToken, BooleanParserToken, MacroParserToken


class TestParserToken:
    """No functionality in base class to test."""


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
