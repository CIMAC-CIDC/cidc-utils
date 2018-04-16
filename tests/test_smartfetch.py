#!/usr/bin/env python3
"""
Unit tests for the SmartFetch class/wrappers
"""

import unittest
from unittest.mock import patch
from cidc_utils.requests import SmartFetch


class TestSmartFetch(unittest.TestCase):
    """[summary]
    
    Arguments:
        unittest {[type]} -- [description]
    """
    def test_smartfetch_fails(self):
        with patch('requests.post') as mock_requests:
            mock_requests.return_value.status_code = 200
            with self.assertRaises(RuntimeError):
                s = SmartFetch('')
                s.post(code=300)

    def test_smartfetch_ok(self):
        with patch('requests.post') as mock_requests:
            mock_requests.return_value.status_code = 200
            s = SmartFetch('')
            s.post(code=200)
