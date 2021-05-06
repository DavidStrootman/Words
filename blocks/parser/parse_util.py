from typing import Iterator

from blocks.helper.token_type_enum import TokenTypeEnum


def eat_until(tokens: Iterator["Token"], limit_type: TokenTypeEnum):
    """Parse tokens until the next token matches the limit_type, leaving the last token unparsed."""
    token = next(tokens)
    if token.value == limit_type:
        return [token]
    parsed_token = token.parse(tokens)
    return [parsed_token] + eat_until(tokens, limit_type)


def eat_until_discarding(tokens: Iterator["Token"], limit_type: TokenTypeEnum):
    """Parse tokens until the next token matches the limit_type, discarding the last token."""
    token = next(tokens)
    if token.value == limit_type:
        return []
    parsed_token = token.parse(tokens)
    return [parsed_token] + eat_until_discarding(tokens, limit_type)
