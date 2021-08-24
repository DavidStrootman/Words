from typing import Iterator, List, Union
from words.helper.TokenTypeEnum import TokenTypeEnum
from words.token_types.parser_token import ParserToken


class Program:
    """
    A collection of parser tokens that can be interpreted or compiled.
    """
    def __init__(self, tokens: List[ParserToken]):
        self.tokens = tokens


def eat_until(tokens: Iterator["LexerToken"], limit_types: List[TokenTypeEnum]) -> List[Union["LexerToken", ParserToken]]:  # noqa: F821, E501
    """
    Parse tokens until the next token matches the limit_type, leaving the last token unparsed.

    :param tokens: The tokens to parse.
    :param limit_types: The types of tokens to stop parsing at.
    :return: List of parser tokens and an unparsed lexer token at the end.
    """
    token = next(tokens)
    if token.value in limit_types:
        return [token]
    parsed_token = token.parse(tokens)
    return [parsed_token] + eat_until(tokens, limit_types)


def eat_until_discarding(tokens: Iterator["LexerToken"], limit_types: List[TokenTypeEnum]) -> List[ParserToken]:  # noqa: F821, E501
    """
    Parse tokens until the next token matches the limit_type, discarding the last token.

    :param tokens: The tokens to parse.
    :param limit_types: The types of tokens to stop parsing at.
    :return: List of parser tokens.
    """
    token = next(tokens)

    if token.value in limit_types:
        return []

    parsed_token = token.parse(tokens)
    return [parsed_token] + eat_until_discarding(tokens, limit_types)
