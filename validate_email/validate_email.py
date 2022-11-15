from .domainlist_check import domainlist_check, return_blacklist
from .email_address import EmailAddress
from .exceptions import AddressFormatError, DomainBlacklistedError
from .regex_check import regex_check
from .tdl import countries

__all__ = ["validate_email_fn"]
__doc__ = """Validate Email Address"""


def validate_email_fn(emailaddress: str, blacklist: set) -> bool:
    value = 0
    try:
        email = EmailAddress(address=emailaddress)
        if email:
            value += 50
        if regex_check(email_address=email):
            value += 50
        if domainlist_check(email_address=email, blacklist=blacklist):
            value += 50
        if email.domain.split(".")[-1] in countries:
            raise DomainBlacklistedError
        else:
            value += 50
    except AddressFormatError:
        value -= 150
    except DomainBlacklistedError:
        value -= 150

    if value > 0:
        return True
    else:
        return False
