from pathlib import Path
import pytest
import sys
from words.interpreter.interpret import Interpreter


class TestExamples:
    @pytest.fixture
    def set_up(self):
        sys.setrecursionlimit(4000)
        self.path_to_examples = Path("examples/words")

    def test_ackermann(self, set_up):
        result = Interpreter.interpret_file(Path("examples/words/ackermann.word"))
        assert result == 125

    def test_fibonacci(self, set_up):
        result = Interpreter.interpret_file(Path("examples/words/fibonacci.word"))
        assert result == 144

    def test_loop(self, set_up):
        result = Interpreter.interpret_file(Path("examples/words/loop.word"))
        assert result == 980700

    def test_rec(self, set_up):
        result = Interpreter.interpret_file(Path("examples/words/rec.word"))
        assert result == True
