import smtplib
from email.mime.text import MIMEText
import ssl
class send_email():
    def __init__(self, recp_eml):
       self.recp_eml = recp_eml
        
    def send(self):
        #sender email
        sender = 'tulpa-hmc-no_reply@outlook.com'
        #receiver email
        receivers = [self.recp_eml]

        port = 587
        msg = MIMEText(""+""+"")
        #Message
        msg['Subject'] = '您的花名册申请未通过审核'
        msg['From'] = 'tulpa-hmc-no_reply@outlook.com'
        msg['To'] = receivers

        #create ssl context for ssl connection to SMTP
        context = ssl.create_default_context()        
        #connect to outlook smtp and send
        with smtplib.SMTP_SSL("smtp.office365.com", port, context) as server:
            server.ehlo() 
            server.starttls()#start TLS connection
            server.login(sender, "c0912c8d3a270ada868bc56862354c8211086af917523e07b60bba30403c6417")#login to SMTP
            server.sendmail(sender, receivers, msg.as_string())#send email via SMTP
            server.close()#close connection
            print("Successfully sent email")