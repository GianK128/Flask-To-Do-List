from flask_mail import Message
from todo_list import mail

def send_email(receivers, subject, template):
    msg = Message(
        subject,
        recipients = [receivers],
        html = template
    )
    mail.send(msg)