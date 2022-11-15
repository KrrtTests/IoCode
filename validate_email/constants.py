from re import IGNORECASE
from re import compile as re_compile

HOST_REGEX = re_compile(
    # max length for domain name labels is 63 characters per RFC 1034
    r'((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+)' +
    r'(?:[A-Z0-9-]{2,63}(?<!-))\Z', IGNORECASE)


USER_REGEX = re_compile(
    # dot-atom
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z" +
    # quoted-string
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013' +
    r'\014\016-\177])*"\Z)', IGNORECASE)
