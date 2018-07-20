#!/usr/bin/env python3
"""
Class that makes interacting with APIs a little bit easier.
"""
from functools import wraps

import requests
from simplejson.errors import JSONDecodeError


def graceful_handling(code: int, token: str=None):
    """
    A wrapper around the requests library that removes the need to write
    error handling behavior for every request

    Arguments:
        code {int} -- HTTP request code indicating a succesful request.
        token {str} -- JWT access token.

    Raises:
        RuntimeError -- Raises a runtime error to indicate a vital request failed.

    Returns:
        requests.Response -- Response object.
    """
    def param_wrap(func):
        """Wrapper around request function.

        Arguments:
            func {[type]} -- [description]

        Raises:
            RuntimeError -- [description]

        Returns:
            [type] -- [description]
        """
        @wraps(func)
        def handle_error(*args, **kwargs):
            """
            Specifies error handling for HTTP requests.

            Raises:
                RuntimeError -- [description]

            Returns:
                [type] -- [description]
            """
            if token:
                if 'headers' in kwargs:
                    kwargs['headers'].update(
                        {'Authorization': 'Bearer {}'.format(token)})
                else:
                    kwargs.update(
                        {'headers': {'Authorization': 'Bearer {}'.format(token)}})
            response = func(*args, **kwargs)
            if not response.status_code == code:
                print("Request Unsuccesful:")
                print(response.reason)
                try:
                    print(response.json())
                except JSONDecodeError:
                    pass
                raise RuntimeError
            return response
        return handle_error
    return param_wrap


class SmartFetch:
    """
    Essentially a wrapper around requests. Adds some handy error catching.
    Allows you to specify a base URL, and automatically adds bearer tokens
    if provided.
    """
    def __init__(self, base_url=''):
        self.base_url = base_url

    def post(self, endpoint: str=None, code: int=200, token: str=None, **kwargs):
        """Wrapper emulating the requests.post method with custom error handling.

        Keyword Arguments:
            endpoint {str} -- API endpoint. (default: {None})
            code {int} -- Status code indicating success. (default: {201})
            token {str} -- JWT access token. (default: {None})

        Returns:
            requests.Response -- HTTP Response.
        """
        return self.do_wrap(requests.post, endpoint=endpoint, code=code, token=token, **kwargs)

    def get(self, endpoint: str=None, code: int=200, token: str=None, **kwargs):
        """Wrapper emulating the requests.get method with custom error handling.

        Keyword Arguments:
            endpoint {str} -- API endpoint. (default: {None})
            code {int} -- Status code indicating success. (default: {200})
            token {str} -- JWT access token. (default: {None})

        Returns:
            requests.Response -- HTTP Response.
        """
        return self.do_wrap(requests.get, endpoint=endpoint, code=code, token=token, **kwargs)

    def patch(self, endpoint: str=None, code: int=200, token: str=None, **kwargs):
        """Wrapper emulating the requests.patch method with custom error handling.

        Keyword Arguments:
            endpoint {str} -- API endpoint. (default: {None})
            code {int} -- Status code indicating success. (default: {200})
            token {str} -- JWT access token. (default: {None})

        Returns:
            requests.Response -- HTTP Response.
        """
        return self.do_wrap(requests.patch, endpoint=endpoint, code=code, token=token, **kwargs)

    def delete(self, endpoint: str=None, code: int=200, token: str=None, **kwargs):
        """Wrapper emulating the requests.delete method with custom error handling.

        Keyword Arguments:
            endpoint {str} -- API endpoint. (default: {None})
            code {int} -- Status code indicating success. (default: {200})
            token {str} -- JWT access token. (default: {None})

        Returns:
            requests.Response -- HTTP Response.
        """
        return self.do_wrap(requests.delete, endpoint=endpoint, code=code, token=token, **kwargs)

    def do_wrap(self, request_func, endpoint: str=None, code=None, token: str=None, **kwargs):
        """
        Wraps the passed request function with the decorator.

        Arguments:
            request_func {object} -- A requests function method.

        Keyword Arguments:
            endpoint {str} -- API endpoint. (default: {None})
            code {int} -- Status code indicating success. (default: {200})
            token {str} -- JWT access token. (default: {None})

        Returns:
            requests.Response -- HTTP Response.
        """
        url = self.base_url

        if endpoint:
            url += '/' + endpoint

        @graceful_handling(code, token)
        def wrapped_request(**kwargs):
            return request_func(url, **kwargs)

        return wrapped_request(**kwargs)
