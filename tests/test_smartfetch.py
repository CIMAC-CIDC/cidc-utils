"""
Unit tests for the SmartFetch class/wrappers
"""

import unittest
from unittest.mock import patch
from cidc_utils.requests import SmartFetch


class TestSmartFetch(unittest.TestCase):
    """Class for testing my "SmartFetch" utility

    Arguments:
        unittest {[type]} -- [description]
    """
    def test_smartfetch_fails(self):
        """
        Test that errors are properly raised on a failed request.
        """
        with patch('requests.post') as mock_requests:
            mock_requests.return_value.status_code = 200
            with self.assertRaises(RuntimeError):
                smart_fetch = SmartFetch('')
                smart_fetch.post(code=300)

    def test_smartfetch_ok(self):
        """[summary]
        """
        with patch('requests.post') as mock_requests:
            mock_requests.return_value.status_code = 200
            smart_fetch = SmartFetch('')
            smart_fetch.post(code=200)
            self.assertIsInstance(smart_fetch, SmartFetch)

def test_smartfetch_instatiate():
    """
    Test the creation of a new SmartFetch object.
    """
    smart_fetch = SmartFetch('')
    assert smart_fetch.base_url == ''

def test_smartfetch_fails():
    """[summary]
    """
    with patch('requests.post') as mock_requests:
        mock_requests.return_value.status_code = 200
        smart_fetch = SmartFetch('')
        value = smart_fetch.post(code=200)
        assert value.status_code == 200
        