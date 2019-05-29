"""
Unit tests for the stackdriver handlers
"""
import os

import pytest
from unittest.mock import patch
from cidc_utils.loghandler import stack_driver_handler


def test_send_mail():
    """Ensure a dummy email can be sent"""
    api_key = os.environ.get("SENDGRID_API_KEY")

    assert api_key, "Must set SENDGRID_API_KEY env variable to run send_mail test"

    assert stack_driver_handler.send_mail(
        "test subject",
        "test message",
        ["cidc@jimmy.harvard.edu"],
        "cidc@jimmy.harvard.edu",
        api_key,
        sandbox_mode=True,
    )
