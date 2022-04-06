import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
load_dotenv()

EmailAddy = os.getenv("EMAIL") #senders Gmail id here
Pass = os.getenv("EMAIL_PASS") #senders Gmail's Password over here 

def sendEmail(subject=None, recipient=None, content=None):

    if subject==None or recipient ==None or content == None:
        print('Required parameters not given')

    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = EmailAddy
    msg['To'] = recipient

    #Generate mail attachment
    part1 = MIMEText(content, "html") #If using html teplate change "plain" to "html"
    #Attach mail
    msg.attach(part1)

    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp: #Added Gmails SMTP Server
        smtp.login(EmailAddy,Pass)
        smtp.sendmail(EmailAddy, recipient, msg.as_string())
        smtp.quit()
        print("Email sent to", recipient)
        del msg['To']
        del msg['From']
        del msg['Subject']

if __name__ == "__main__":
    sendEmail("Test email", "example@example.com","This is some test content")