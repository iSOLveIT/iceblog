# Local modules
from datetime import datetime as dt
import os

# User-defined modules
from content import mail

# Third-party modules
from flask_mail import Message


def send_email(_name, _subject, _email, _body):
    
    # SEND EMAIL
    _recipient = str(os.environ.get('MAIL_USERNAME'))
    msg = Message(_subject, sender=('IceBlog Contact', str(os.environ.get('MAIL_USERNAME'))), recipients=[_recipient])
    msg.body = f'''{_body}


Sender's Name: {_name}
Sender's Email: {_email}
Date Sent:  {dt.now().strftime('%B %d, %Y, %H:%M ') + 'GMT'}
'''
    mail.send(msg)
    return 'OK'


def reply_message(_email, _sender):
    # REPLY EMAIL
    _subj = 'Message Received'
    msg = Message(_subj, sender=('IceBlog Contact', str(os.environ.get('MAIL_USERNAME'))), recipients=[_email])
    msg.body = f'''Hello {_sender},
The message sent by {_sender} to IceBlog has been received. IceBlog will contact you within 24 hours.

Thank you,
IceBlog Team.

Date Sent:  {dt.now().strftime('%B %d, %Y, %H:%M ') + 'GMT'}
'''
    mail.send(msg)
    return 'OK'
