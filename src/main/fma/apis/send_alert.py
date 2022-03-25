from src.main.fma.controllers import users_db
import smtplib


# username: fma.finalproject2022@yahoo.com
# password: lidarzahomer7
# app-password: zkykgdjwieuikyrf
class send_alert:
    def __init__(self):
        self.email_address = 'fma.finalproject2022@yahoo.com'
        self.subject = 'Subject: We Found New Apartments For You!\n\n'
        self.passcode = 'zkykgdjwieuikyrf'
        self.content = 'Hello, \n We are glad to tell you that after a long long search we found some apartments that can interest you.\nPlease click the link: \n{url}\n\n.'
        self.footer = "Thank you."
        self.conn = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)
        self.conn.ehlo()
        self.conn.login(self.email_address, self.passcode)

    def find_all_users_id(self):
        emails = []
        users = users_db.find({})
        for user in users:
            emails.append(user['id'])
        return emails

    def send_email_with_update(self):
        users_email = self.find_all_users_id()
        for email in users_email:
            self.conn.sendmail(self.email_address,
                               email,
                               self.subject + self.content + self.footer)
        self.conn.quit()


# s = send_alert()
# s.find_all_users_id()
