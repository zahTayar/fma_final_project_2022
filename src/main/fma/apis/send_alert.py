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
        self.content = 'Hello, \nWe are glad to tell you that after a long long search we found some apartments that can interest you.\nPlease click the link: \nhttp://localhost:3000/history\n\n.'
        self.footer = "Thank you."

    def find_all_users_id(self):
        emails = []
        users = users_db.find({})
        if not users:
            return None
        for user in users:
            emails.append(user['email'])
        return emails

    def send_email_with_update(self):
        global conn
        users_email = self.find_all_users_id()
        try:
            conn = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)
            conn.ehlo()
            conn.login(self.email_address, self.passcode)
        except smtplib.SMTPException as e:
            print(e)
        if users_email is None:
            print('There are no users in the system')
            return
        for email in users_email:
            try:
                conn.sendmail(self.email_address,
                              email,
                              self.subject + self.content + self.footer)
            except smtplib.SMTPException as e:
                print(e)
                conn.quit()
        conn.quit()

