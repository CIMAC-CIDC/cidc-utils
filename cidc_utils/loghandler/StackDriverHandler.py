#!/usr/bin/env python3
"""
A custom class to send formatted logs to Stackdriver
"""
import logging
from typing import List
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail, Personalization
from pythonjsonlogger import jsonlogger


def add_recipients(mail_object: Mail, recipients: List[str]) -> None:
    """
    Takes a sendgrid mail object and adds a list of e-mails as blind-copy recipients.

    Arguments:
        mail_object {Mail} -- Mail object respresenting e-mail.
        recipients {List[str]} -- String list of e-mails to be sent to.
    """
    personalization = Personalization()
    [personalization.add_bcc(Email(address)) for address in recipients]
    mail_object.add_personalization(personalization)


def send_mail(
        subject: str,
        message_text: str,
        to_emails: List[str],
        send_from_email: str,
        sendgrid_api_key: str
) -> bool:
    """
    Send an email via Sendgrid. Configure API_KEY via constants.

    Arguments:
        subject {str} -- Subject line of email.
        message_text {str} -- Text of email.
        to_emails {List[str]} -- Destination email. The first element in the list will be
        considered the primary recipient.

    Returns:
        bool -- True if succesful.
    """
    sg = sendgrid.SendGridAPIClient(sendgrid_api_key)
    from_email = Email(send_from_email)
    to_email = Email(to_emails[0])
    subject = subject
    content = Content("text/plain", message_text)
    mail = Mail(from_email, subject, to_email, content)

    # Add all other e-mail addresses as BCC.
    add_recipients(mail, to_emails[1:])
    response = sg.client.mail.send.post(request_body=mail.get())

    return response.status_code == 202


class StackdriverJsonFormatter(jsonlogger.JsonFormatter, object):
    """
    Inherits from the JonFormatter class, this is a custom formatter
    to cause google to correctly visually distinguish between alert levels,
    and to ensure that users logging errors are appropriately
    tagging their alerts.

    Arguments:
        jsonlogger {jsonlogger.JsonFormatter} -- [description]
        object {object} -- [description]
    """

    _sendgrid_api_key = None
    _send_from_email = None
    _to_emails = None

    def __init__(self, fmt="%(levelname) %(message)", style='%', *args, **kwargs):
        jsonlogger.JsonFormatter.__init__(self, fmt=fmt, *args, **kwargs)

    def configure_sendgrid(self, api_key: str, from_email: str, to_emails: List[str]) -> None:
        """
        Function to configure sendgrind credentials

        Arguments:
            api_key {[type]} -- [description]
            from_email {[type]} -- [description]
            to_emails {[str]} -- List of e-mail addresses to send the mail to.
        """
        self._send_from_email = from_email
        self._sendgrid_api_key = api_key
        self._to_emails = to_emails

    def process_log_record(self, log_record):
        log_record['severity'] = log_record['levelname']

        # If the log is tagged as "e-mail" send it out.
        if 'category' in log_record and 'EMAIL' in log_record['category'] and (
                self._send_from_email and self._sendgrid_api_key and self._to_emails):
            send_mail(
                'STACKDRIVER_NOTIFICATION',
                log_record['message'],
                self._to_emails,
                self._send_from_email,
                self._sendgrid_api_key
            )

        del log_record['levelname']
        return super(StackdriverJsonFormatter, self).process_log_record(log_record)

    def add_fields(self, log_record, record, message_dict):
        super(StackdriverJsonFormatter, self).add_fields(log_record, record, message_dict)
        if 'category' not in message_dict:
            message_dict['category'] = 'INFO'
        log_record['category'] = message_dict['category']
