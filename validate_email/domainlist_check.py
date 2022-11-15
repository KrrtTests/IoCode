from pathlib import Path
from tempfile import gettempdir
from time import time

import requests

from .email_address import EmailAddress
from .exceptions import DomainBlacklistedError


def return_blacklist() -> set:
    'Return the domain blacklist.'
    BLACKLIST_URL = 'https://raw.githubusercontent.com/disposable-email-domains/disposable-email-domains/master/disposable_email_blocklist.conf'
    TMP_PATH = Path(gettempdir()).joinpath('validate-email-blacklist.txt')
    if not TMP_PATH.exists():
        TMP_PATH.touch()

    _refresh_when_older_than: int = 5 * 24 * 60 * 60  # 5 days
    true_when_older_than = time() - _refresh_when_older_than
    if true_when_older_than or TMP_PATH.stat().st_size == 0:
        with requests.get(BLACKLIST_URL) as response:
            response.raise_for_status()
            TMP_PATH.write_text(response.text)

    with open(TMP_PATH, 'r') as f:
        domain_blacklist = f.read().splitlines()

    return set(x.strip().lower() for x in domain_blacklist)


def domainlist_check(email_address: EmailAddress, blacklist: set) -> bool:
    'Check the provided email against domain lists.'
    if email_address.domain in blacklist:
        raise DomainBlacklistedError
    return True
