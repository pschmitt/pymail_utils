#!/usr/bin/env python
# coding: utf-8


import argparse
import logging
from email.mime.text import MIMEText
from smtplib import SMTP
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
import sys


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def send_mail(sender, password, recipient, subject, message, attachments=None,
              smtp_server='smtp.dt.ept.lu', smtp_port=25):
    logger.debug(
        'Send mail via {}:{} From: {} To: {}'.format(
            smtp_server, smtp_port, sender, recipient
        )
    )
    msg = MIMEMultipart()

    recipients = recipient if type(recipient) is list else [recipient]

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)  # msg['To'] can only contain a string

    body = MIMEText(message)
    msg.attach(body)

    if attachments:
        for k, v in attachments.iteritems():
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(v, 'rb').read())
            Encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition', 'attachment; filename="{}"'.format(k)
            )
            msg.attach(part)

    logger.debug(msg)

    s = SMTP(smtp_server, port=smtp_port)
    s.starttls()
    s.login(sender, password)
    s.sendmail(sender, recipients, msg.as_string())
    s.quit()


def parse_args():
    parser = argparse.ArgumentParser(description='Process args')
    parser.add_argument(
        '-S', '--smtp',
        required=False,
        action='store',
        default='smtp.dt.ept.lu',
        help='SMTP Server'
    )
    parser.add_argument(
        '-P', '--port',
        required=False,
        action='store',
        default=25,
        type=int,
        help='SMTP Server Port'
    )
    parser.add_argument(
        '-s', '--sender',
        required=True,
        action='store',
        help='Email of the sender'
    )
    parser.add_argument(
        '-p', '--password',
        required=True,
        action='store',
        help='Password of the account'
    )
    parser.add_argument(
        '-r', '--recipient',
        action='append',
        required=True,
        help='Recipient of the mail'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        default=False,
        help='Verbose output'
    )
    parser.add_argument(
        '-D', '--debug',
        action='store_true',
        help=argparse.SUPPRESS
    )
    parser.add_argument(
        '-a', '--attachment',
        action='append',
        required=False,
        type=argparse.FileType('r'),
        help='Attachment'
    )
    parser.add_argument('SUBJECT')
    parser.add_argument('MESSAGE')
    return parser.parse_args()

def main():
    args = parse_args()
    attachments = {}
    if args.attachment:
        for a in args.attachment:
            attachments[a.name] = a.name
    send_mail(
        smtp_server=args.smtp,
        smtp_port=args.port,
        sender=args.sender,
        password=args.password,
        recipient=args.recipient,
        subject=args.SUBJECT,
        message=args.MESSAGE,
        attachments=attachments
    )


if __name__ == '__main__':
    sys.exit(main())
