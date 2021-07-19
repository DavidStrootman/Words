from typing import Iterator, List, TypeVar
from words.helper.token_type_enum import TokenTypeEnum
from words.token.parser_token import ParserToken


class Program:
    def __init__(self, tokens: List[ParserToken]):
        self.tokens = tokens


TOKEN = TypeVar('TOKEN', ParserToken, "LexerToken")


def eat_until(tokens: Iterator["LexerToken"], limit_types: List[TokenTypeEnum]) -> List[TOKEN]:
    """Parse tokens until the next token matches the limit_type, leaving the last token unparsed."""
    token = next(tokens)
    if token.value in limit_types:
        return [token]
    parsed_token = token.parse(tokens)
    return [parsed_token] + eat_until(tokens, limit_types)


def eat_until_discarding(tokens: Iterator["LexerToken"], limit_types: List[TokenTypeEnum]) -> List[ParserToken]:
    """Parse tokens until the next token matches the limit_type, discarding the last token."""
    token = next(tokens)
    if token.value in limit_types:
        return []
    parsed_token = token.parse(tokens)
    return [parsed_token] + eat_until_discarding(tokens, limit_types)
