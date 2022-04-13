from pathlib import Path
import pytest
import sys
from words.interpreter.interpret import Interpreter


class TestExamples:
    @pytest.fixture
    def set_up(self):
        sys.setrecursionlimit(4000)
        self.path_to_examples = Path("examples/words")

    @pytest.mark.xfail(reason="Examples change often, giving different outputs.")
    def test_ackermann(self, set_up):
        result = Interpreter.interpret_file(Path("examples/words/ackermann.word"), init=[])
        assert result == 125

    @pytest.mark.xfail(reason="Examples change often, giving different outputs.")
    def test_fibonacci(self, set_up):
        result = Interpreter.interpret_file(Path("examples/words/fibonacci.word"), init=[])
        assert result == 144

    @pytest.mark.xfail(reason="Examples change often, giving different outputs.")
    def test_loop(self, set_up):
        result = Interpreter.interpret_file(Path("examples/words/loop.word"), init=[])
        assert result == 980700

    @pytest.mark.xfail(reason="Examples change often, giving different outputs.")
    def test_rec(self, set_up):
        result = Interpreter.interpret_file(Path("examples/words/rec.word"), init=[])
        assert result is True
