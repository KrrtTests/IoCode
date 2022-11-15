
from .constants import HOST_REGEX, USER_REGEX
from .email_address import EmailAddress


def regex_check(email_address: EmailAddress) -> bool:
    '''
    Slightly adjusted email regex checker from the Django project.
    '''
    if USER_REGEX.match(email_address.user) and HOST_REGEX.match(email_address.ace_domain):
        return True
    else:
        return False