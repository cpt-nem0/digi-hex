import os
from dotenv import load_dotenv
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

message = MIMEMultipart()
message["from"] = "Test User"
message["to"] = "rohanya.76426@gmail.com"
message["subject"] = "Test mail check" 
message.attach(MIMEText("Body"))

try:
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login("{}".format(os.getenv('TEST_EMAIL')), "{}".format(os.getenv('TEST_EMAIL_PASSWORD')))
        smtp.send_message(message)
        print("message sent successfully...")

except:
    print("message was not...")