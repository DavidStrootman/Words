from typing import Iterator, List, Tuple, Dict

from words.interpreter.interpret_util import exhaustive_interpret_tokens
from words.lexer.lex import Lexer
from words.parser.parse import Parser
from words.token_types.lexer_token import LexerToken
from words.token_types.parser_token import ParserToken


def parse_from_string(words: str) -> List[ParserToken]:
    contents_with_line_nums = enumerate(iter(words.splitlines()))
    lexed_tokens: Iterator[LexerToken] = Lexer.lex_file_contents(contents_with_line_nums)
    return Parser.parse(lexed_tokens).tokens


def execute_from_string(words: str) -> Tuple[List[ParserToken], Dict[str, ParserToken]]:
    contents_with_line_nums = enumerate(iter(words.splitlines()))
    lexed_tokens: Iterator[LexerToken] = Lexer.lex_file_contents(contents_with_line_nums)
    return exhaustive_interpret_tokens(Parser.parse(lexed_tokens).tokens, [], {})
