from __future__ import unicode_literals


class ApiError(Exception):
    pass


class AuthError(ApiError):
    pass


class ApiConnectionError(ApiError):
    message = 'Order API connection error'
