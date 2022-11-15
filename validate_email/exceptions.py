class Error(Exception):
    'Base class for all exceptions of this module.'
    message = 'Unknown error.'

    def __str__(self):
        return self.message


class ParameterError(Error):
    """
    Base class for all exceptions indicating a wrong function parameter.
    """


class FromAddressFormatError(ParameterError):
    """
    Raised when the from email address used for the MX check has an
    invalid format.
    """
    message = 'Invalid "From:" email address.'


class EmailValidationError(Error):
    'Base class for all exceptions indicating validation failure.'


class AddressFormatError(EmailValidationError):
    'Raised when the email address has an invalid format.'
    message = 'Invalid email address.'


class DomainBlacklistedError(EmailValidationError):
    """
    Raised when the domain of the email address is blacklisted on
    https://github.com/disposable-email-domains/disposable-email-domains.
    """
    message = 'Domain blacklisted.'


class DNSError(EmailValidationError):
    """
    Base class of all exceptions that indicate failure to determine a
    valid MX for the domain of email address.
    """


class DomainNotFoundError(DNSError):
    'Raised when the domain is not found.'
    message = 'Domain not found.'


class NoNameserverError(DNSError):
    'Raised when the domain does not resolve by nameservers in time.'
    message = 'No nameserver found for domain.'


class DNSTimeoutError(DNSError):
    'Raised when the domain lookup times out.'
    message = 'Domain lookup timed out.'


class DNSConfigurationError(DNSError):
    """
    Raised when the DNS entries for this domain are falsely configured.
    """
    message = 'Misconfigurated DNS entries for domain.'


class NoMXError(DNSError):
    'Raised when the domain has no MX records configured.'
    message = 'No MX record for domain found.'


class NoValidMXError(DNSError):
    """
    Raised when the domain has MX records configured, but none of them
    has a valid format.
    """
    message = 'No valid MX record for domain found.'


class TLSNegotiationError(EmailValidationError):
    'Raised when an error happens during the TLS negotiation.'
    _str = 'During TLS negotiation, the following exception(s) happened: {exc}'

    def __str__(self):
        'Print a readable depiction of what happened.'
        return self._str.format(exc=', '.join(repr(x) for x in self.args))
