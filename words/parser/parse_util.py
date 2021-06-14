from typing import Iterator, List
from words.helper.token_type_enum import TokenTypeEnum
from words.token.parser_token import ParserToken


class Program:
    def __init__(self, tokens: List[ParserToken]):
        self.tokens = tokens


def eat_until(tokens: Iterator["LexerToken"], limit_type: TokenTypeEnum):
    """Parse tokens until the next token matches the limit_type, leaving the last token unparsed."""
    token = next(tokens)
    if token.value == limit_type:
        return [token]
    parsed_token = token.parse(tokens)
    return [parsed_token] + eat_until(tokens, limit_type)


def eat_until_discarding(tokens: Iterator["LexerToken"], limit_type: TokenTypeEnum):
    """Parse tokens until the next token matches the limit_type, discarding the last token."""
    token = next(tokens)
    if token.value == limit_type:
        return []
    parsed_token = token.parse(tokens)
    return [parsed_token] + eat_until_discarding(tokens, limit_type)
