
import smtplib, ssl
from settings import Settings
from email.mime.text import MIMEText

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

        try:
            # Sätter upp en server som man skickar mailen från
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
            print("Sending mails failed with following exception: " + str(e))
            return False

if __name__ == '__main__':
    s = Settings()
    mails = ['Sofia@reineck.se ', 'clas.zachrisson99@gmail.com', 'oliver@kraften.net', 'kottsky@gmail.com', 'Lovisj01@hotmail.com ', ' moaet25@gmail.com', 'martin.knebel.e@gmail.com', 'Melker.ernfors@gmail.com ', 'Elsamayspengler@gmail.com ', 'samsamv02@gmail.com', 'Felicia.L.Bengtsson@gmail.com ', 'anton.onils@gmail.com', 'sofia.ekbring@gmail.com', 'Lindholmcarlaxel@gmail.com ', 'svenssondahl@gmail.com', 'Sofiakvist050@gmail.com', 'sofia63.naslund@hotmail.se', 'alva.b.99@live.se', 'alice.gardell@icloud.com', 'ninap21@hotmail.com', 'hasztely@gmail.com', 'karinida.haglund@gmail.com ', 'Elias5@live.se ', 'alicialaurinen@outlook.com', 'emil.vendlegard@gmail.com', 'Kalle.johansson14@gmail.com', 'fabianlindblad@hotmail.se ', 'sofie.s.skold@gmail.com', 'gabrieleriksvensson@gmail.com', 'johan.wallsten@hotmail.com', 'erik.n.nilsson.98@gmail.com', 'Pappannadorottya@gmail.com', 'tovemaria.moller@gmail.com', 'Alex_chelsea@hotmail.se', 'Belmavila@gmail.com', 'Clarakriegholm@gmail.com', '2002vali@gmail.com']
    mailss = {mail: s.mysk_mail for mail in mails}

    ml = MailSender(s.password, s.sender_email)

    ml.bulk_send(mailss, 'Bekräftelse')
