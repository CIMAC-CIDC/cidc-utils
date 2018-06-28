#!/usr/bin/env python3
"""
A custom class to send formatted logs to Stackdriver
"""
from pythonjsonlogger import jsonlogger


class StackdriverJsonFormatter(jsonlogger.JsonFormatter, object):
    """
    Inherits from the JonFormatter class, this is a custom formatter
    to cause google to correctly visually distinguish between alert levels,
    and to ensure that users logging errors are appropriately
    tagging their alerts.

    Arguments:
        jsonlogger {[type]} -- [description]
        object {[type]} -- [description]
    """

    def __init__(self, fmt="%(levelname) %(message)", style='%', *args, **kwargs):
        jsonlogger.JsonFormatter.__init__(self, fmt=fmt, *args, **kwargs)

    def process_log_record(self, log_record):
        log_record['severity'] = log_record['levelname']
        del log_record['levelname']
        return super(StackdriverJsonFormatter, self).process_log_record(log_record)

    def add_fields(self, log_record, record, message_dict):
        super(StackdriverJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not message_dict['category']:
            raise ValueError(
                'Improperly formatted log. Please remember to add a category definition')
        log_record['category'] = message_dict['category']
