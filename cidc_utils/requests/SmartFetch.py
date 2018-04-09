#!/usr/bin/env python3
"""
Class that makes interacting with APIs a little bit easier.
"""
import requests
from functools import wraps
from urllib.error import HTTPError
from simplejson.errors import JSONDecodeError


def graceful_handling(code):
    """
    A wrapper around the requests library that removes the need to write
    error handling behavior for every request

    Arguments:
        code {int} -- HTTP request code indicating a succesful request.

    Raises:
        RuntimeError -- [description]

    Returns:
        [type] -- [description]
    """
    def param_wrap(func):
        @wraps(func)
        def handle_error(*args, **kwargs):
            if 'token' in kwargs:
                kwargs['headers'].update({'Authorization': 'Bearer {}'.format(kwargs['token'])})
            response = func(*args, **kwargs)
            success = response.status_code == code if 'code' not in kwargs \
                else kwargs['code'] == response.status_code
            if not success:
                print("Request Unsuccesful:")
                print(response.reason)
                try:
                    print(response.json())
                except JSONDecodeError:
                    pass
                raise RuntimeError
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

    @graceful_handling(201)
    def post(self, url='', **kwargs):
        full_path = self.base_url + url
        return requests.post(full_path, **kwargs)

    @graceful_handling(200)
    def get(self, url='', **kwargs):
        full_path = self.base_url + url
        return requests.post(full_path, **kwargs)

    @graceful_handling(200)
    def patch(self, url='', **kwargs):
        full_path = self.base_url + url
        return requests.patch(full_path, **kwargs)

    @graceful_handling(200)
    def delete(self, url='', **kwargs):
        full_path = self.base_url + url
        return requests.delete(full_path, **kwargs)
