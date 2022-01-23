
import smtplib, ssl
from email.mime.text import MIMEText

class MailSender:

    def __init__(self, password, sender_email):
        self.port = 465  # For SSL
        self.smtp_server = "smtp.gmail.com" # For using Gmail
        self.sender_email = sender_email
        self.password = password

        self.context = ssl.create_default_context()

    def bulk_send(self, mails: dict, subject = '') -> bool:
        '''Sends emails in mails. mails is a dictionary
        where the key is an email and the value is the text to be sent.
        '''

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context = self.context) as server:
                server.login(self.sender_email, self.password)
                for receiver_email, message in mails.items():
                    msg = MIMEText(message, 'html')
                    msg['Subject'] = subject
                    msg['From'] = self.sender_email
                    msg['To'] = receiver_email
                    server.sendmail(self.sender_email, receiver_email, msg.as_string())
            return True
        except Exception as e:
            print("Sending mails failed with following exception: " + e)
            return False

if __name__ == '__main__':
    mail = MailSender('futftuppen1', 'schemacykelsittning@gmail.com')
    msg = "Subject: SCHEMA\
            Här kommer ditt schema för kvällen!!\n\
            Du kommer ha stoppen [stopp1] -> [stopp2] -> [stopp3].\
            Du som värd har gäster med följande matpreferenser:\n\t [foodpreference]\n\
            och följande alkoholpreferenser:\n\t [alcoholpreference]\n\
            Vänligt halsande!"
 
    mail.bulk_send({'tyra_axen@hotmail.se' : msg})