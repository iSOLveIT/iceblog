from flask_mail import Message
from datetime import datetime as dt
from flask import jsonify
from content import mail


def sendEmail(_name, _subject, _email, _body):
    # SEND EMAIL
    _recipient = 'isolveitgroup@gmail.com'
    msg = Message(_subject, sender=('iSOLveIT Contact', 'isolveitgroup@gmail.com'), recipients=[_recipient])
    msg.body = f'''{_body}


Sender's Name: {_name}
Sender's Email: {_email}
Date Sent:  {dt.now().strftime('%B %d, %Y, %H:%M ') + 'GMT'}
'''
    mail.send(msg)
    return 'OK'


def replyMessage(_email, _sender):
    # REPLY EMAIL
    _subj = 'Message Received'
    mesg = Message(_subj, sender=('iSOLveIT Contact', 'isolveitgroup@gmail.com'), recipients=[_email])
    mesg.body = f'''Hello {_sender},
The message sent by {_sender} to iSOLveIT has been received. iSOLveIT will contact you within 24 hours.

Thank you,
iSOLveIT Team.

Date Sent:  {dt.now().strftime('%B %d, %Y, %H:%M ') + 'GMT'}
'''
    mail.send(mesg)
    return 'OK'
