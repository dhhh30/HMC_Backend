import smtplib
from email.mime.text import MIMEText

class send_email:
    def __init__(self, recp_eml):
       self.recp_eml = recp_eml
        
    def send(self):
        sender = 'tulpa-hmc-no_reply@outlook.com'
        receivers = [self.recp_eml]


        port = 1025
        msg = MIMEText('This is test mail')

        msg['Subject'] = 'Test mail'
        msg['From'] = 'admin@example.com'
        msg['To'] = 'info@example.com'
        #connect to outlook smtp and send
        with smtplib.SMTP("smtp.office365.com", port) as server:
            server.login(sender, "c0912c8d3a270ada868bc56862354c8211086af917523e07b60bba30403c6417")
            server.sendmail(sender, receivers, msg.as_string())
            print("Successfully sent email")