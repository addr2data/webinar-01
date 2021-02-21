"""Exceptions for awshelper package."""


class AwsHelperError(Exception):
    # Exception class for VxRail interface.

    def __init__(self, message):
        err_msg = 'error:  ' + message
        super().__init__(err_msg)
