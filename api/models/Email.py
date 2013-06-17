import smtplib
from email.mime.text import MIMEText
from models import Logger
import settings

class Email:
    
    def __init__(self, sender=None, recipient=None):
        self.host = settings.EMAILHOST
        self.sender = sender or settings.EMAILSENDER
        self.recipient = recipient or settings.EMAILRECIPIENT
    
    def send(self, subject, body):
        msg = MIMEText(body, 'html')
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = self.recipient
        
        try:
            s = smtplib.SMTP(self.host)
            if settings.EMAILUSERNAME and settings.EMAILPASSWORD:
                s.login(settings.EMAILUSERNAME, settings.EMAILPASSWORD)
            s.sendmail(self.sender, self.recipient, msg.as_string())
        except:
            Logger.log_to_file(msg.as_string())
        