
import smtplib, ssl
from settings import Settings
from email.mime.text import MIMEText
from time import sleep
from pprint import pprint

class MailSender:

    def __init__(self, password: str, sender_email: str):
        self.port = 465  # For SSL
        self.smtp_server = "smtp.gmail.com" # For using Gmail
        self.sender_email = sender_email
        self.password = password

        self.context = ssl.create_default_context()

    def bulk_send(self, mails: dict, subject = '') -> bool:
        '''Sends emails in mails. mails is a dictionary
        where the key is an email and the value is the text to be sent.
        '''
        # Safety precaution
            # Sätter upp en server som man skickar mailen från
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context = self.context) as server:
            server.login(self.sender_email, self.password)
            for receiver_email, message in mails.items():
                msg = MIMEText(message, 'html')
                msg['Subject'] = subject
                msg['From'] = self.sender_email
                msg['To'] = receiver_email
                try:
                    server.sendmail(self.sender_email, receiver_email, msg.as_string())
                except Exception as e:
                    print("Sending mails failed with following exception: " + str(e))
                    print(f"Mail should have gone to {receiver_email}:\n\
                        {msg.as_string()}")
                sleep(1)
            return True
            return False

if __name__ == '__main__':
    s = Settings()
    mails = ['martincsvardsjo@gmail.com']
    mailss = {mail: s.mail_template for mail in mails}
    ml = MailSender(s.password, s.sender_email)

    ml.bulk_send(mailss, 'Bekräftelse')
