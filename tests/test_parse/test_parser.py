from words.parser.parse import Parser
from words.token_types.lexer_token import LexerToken, IdentLexerToken
from words.token_types.parser_token import IdentParserToken
from words.lexer.lex_util import DebugData, Word


class TestParser:
    def test_parse_positive(self):
        """Test parsing some tokens."""
        parser = Parser()
        tokens = iter([IdentLexerToken(Word("TEST_VAR", DebugData(0))),
                       IdentLexerToken(Word("TEST_VAR2", DebugData(0)))])
        program = parser.parse(tokens)

        assert isinstance(program.tokens[0], IdentParserToken)
        assert isinstance(program.tokens[1], IdentParserToken)
