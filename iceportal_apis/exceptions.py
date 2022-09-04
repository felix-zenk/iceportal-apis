#!/usr/bin/env python
"""
Exceptions for iceportal_apis
"""

from onboardapis.exceptions import OnboardException


################################################
class ApiException(OnboardException):
    def __init__(self, message):
        """
        Base exception for this module
        """
        super(ApiException, self).__init__(message)


class NetworkException(ApiException):
    """Exception raised when a request fails to fetch data from the api

    Attributes:
        url -- the url that caused the error
        message -- explanation of the error
    """

    def __init__(self, url=None, message='Could not fetch correct data from the server'):
        self.url = url
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        if self.url is not None:
            return f'Could not fetch correct data from "{self.url}"'
        else:
            return self.message


class NotOnTrainException(ApiException):
    """Exception raised when the request returns a website and no json data
    """

    def __init__(self, message='You have to be on a train to use this function'):
        super().__init__(message)


class NotAvailableException(ApiException):
    """Exception raised when specific content is not available through the api
    """

    def __init__(self, message='This data is currently not available on the server'):
        super().__init__(message)


class NotInFutureException(ApiException):
    """Exception raised when a timedelta object is negative but only a positive value is allowed
    """

    def __init__(self, message='This event took place in the past, while only future events are allowed'):
        super().__init__(message)


class NoneDataException(ApiException):
    """Exception raised when a requested element returns None
    """

    def __init__(self, message='The requested data returned None'):
        super().__init__(message)


class MissingArgumentError(TypeError):
    """Error raised when a function has optional parameters of which at least one has to be supplied but none were supplied
    """

    def __init__(self, message='Missing at least one argument: station_name, evaNr'):
        super().__init__(message)
################################################
