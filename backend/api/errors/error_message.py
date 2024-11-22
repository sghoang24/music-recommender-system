# pylint: disable=E0401
"""Error Messages."""


class BaseErrorMessage:
    """Base error message."""

    status_code: int
    message_code: int
    message: str

    def __init__(self, message, status_code=500, message_code=0):
        self.status_code = status_code
        self.message_code = message_code
        self.message = message


class EmailRegisteredError(BaseErrorMessage):
    """Email registered error."""

    status_code = 404
    message_code = 1
    message = "Email already registered."


class SentEmailError(BaseErrorMessage):
    """Sent email error."""

    status_code = 500
    message_code = 2
    message = "Failed to send email."


class TokenDecodingError(BaseErrorMessage):
    """Token decoding error."""

    status_code = 400
    message_code = 3
    message = "Token decoding error"


class UserNotFoundError(BaseErrorMessage):
    """User not found error."""

    status_code = 404
    message_code = 4
    message = "User not found"


class ExpiredSignatureError(BaseErrorMessage):
    """Expired signature error."""

    status_code = 404
    message_code = 5
    message = "Expired signature error"


class EmailNotExistError(BaseErrorMessage):
    """Email does not exist."""

    status_code = 404
    message_code = 6
    message = "Email does not exist"


class TokenNotExistError(BaseErrorMessage):
    """Token does not exist."""

    status_code = 404
    message_code = 7
    message = "Token does not exist"


class UnverifiedAccountEmail(BaseErrorMessage):
    """Unverified account email."""

    status_code = 404
    message_code = 8
    message = "Unverified account email"


class IncorrectEmailOrPassword(BaseErrorMessage):
    """Incorrect email or password."""

    status_code = 404
    message_code = 9
    message = "Incorrect email or password"


class VerifiedEmail(BaseErrorMessage):
    """Verified email."""

    status_code = 404
    message_code = 10
    message = "Verified email."
