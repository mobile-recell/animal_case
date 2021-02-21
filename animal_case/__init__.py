from typing import Dict, List, Union, Iterable
import re


from .types import SNAKE_CASE, CAMEL_CASE, PASCAL_CASE


def _unpack(data) -> Iterable:
    if isinstance(data, dict):
        return data.items()
    return data


def to_snake_case(value: str) -> str:
    """
    Convert camel case string to snake case
    :param value: string
    :return: string
    """
    first_underscore = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', first_underscore).lower()


def keys_to_snake_case(content: Dict) -> Dict:
    """
    Convert all keys for given dict to snake case
    :param content: dict
    :return: dict
    """
    return {to_snake_case(key): value for key, value in _unpack(content)}


def to_pascal_case(value: str, ignore_pattern =None) -> str:
    """
    Convert camel case string to pascal case
    :param value: string
    :return: string
    """
    content = value.split('_')
    if len(content) == 1:
        if ignore_pattern and ignore_pattern.match(content[0]):
            return content[0]
        else:
            return content[0].title()
    else:
        return ''.join(word.title() for word in content[0:] if not word.isspace())


def keys_to_pascal_case(content: Dict, ignore_pattern=None) -> Dict:
    """
    Convert all keys for given dict to pascal case
    :param content: dict
    :return: dict
    """
    return {to_pascal_case(key, ignore_pattern): value for key, value in _unpack(content)}


def to_camel_case(value: str) -> str:
    """
    Convert the given string to camel case
    :param value: string
    :return: string
    """
    content = value.split('_')
    return content[0] + ''.join(word.title() for word in content[1:] if not word.isspace())


def keys_to_camel_case(content: Dict) -> Dict:
    """
    Convert all keys for given dict to camel case
    :param content: dict
    :return: dict
    """
    return {to_camel_case(key): value for key, value in _unpack(content)}


def parse_keys(data: Union[Dict, List] = None, types=SNAKE_CASE, ignore_pattern = None) -> Union[Dict, List]:
    """
    Convert all keys for given dict/list to snake case recursively
    the main type are 'snake' and 'camel'
    :param data: dict | list
    :return: dict | list
    """
    if types not in (SNAKE_CASE, CAMEL_CASE, PASCAL_CASE):
        raise ValueError("Invalid parse type, use snake or camel")
    
    if not isinstance(data, (list, dict)):
        raise TypeError("Invalid data type, use list or dict")
    if types == 'snake':
        formatter = keys_to_snake_case
    elif types == 'camel':
        formatter = keys_to_camel_case
    else:
        formatter = keys_to_pascal_case
    formatted = type(data)()

    is_dict = lambda x: type(x) == dict
    is_list = lambda x: type(x) == list

    for key, value in _unpack(formatter(data, ignore_pattern)):
        if is_dict(value):
            val = value
            if isinstance(value, (list, dict)):
                val = parse_keys(value, types, ignore_pattern=ignore_pattern)
            formatted[key] = val

        elif is_list(value) and len(value) > 0:
            formatted[key] = []
            for val in value:
                if isinstance(val, (list, dict)):
                    val = parse_keys(val, types, ignore_pattern=ignore_pattern)
                formatted[key].append(val)
        else:
            formatted[key] = value
    return formatted
