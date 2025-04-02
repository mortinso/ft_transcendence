# Description: Custom exceptions for OAuth authentication.

class OauthAuthenticationError(Exception):
    def __init__(self, message, status=401):
        self.message = message
        self.status = status
        super().__init__(message)
