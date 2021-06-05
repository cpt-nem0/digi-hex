import os
import smtplib

from ledger import message
from ledger.schema import *

from email.mime.text import MIMEText

from flask import session

from dotenv import load_dotenv

load_dotenv()
# message = MIMEMultipart()

def send_mail(clientMail, amount, remarks):

    user = Businesses.objects(b_id=session['user_id']).first()
    cEmails = [x.clientEmail for x in user.clients]

    message["from"] = f"{user.b_owner}"
    message["to"] = clientMail
    message["subject"] = "Payment Request" 
    cName = user.clients[cEmails.index(clientMail)].clientName
    link = generateLink(link='/confirmPayment/clientMail')
    msg = f'''
    <!DOCTYPE html>
    <html lang="en">

    <head>
    </head>

    <body>
        <p>Hi {cName},<br><br>

        {session['user']} has requested payment,<br>
        Details of the transaction:<br><br>

        <u>Amount:</u> Rs. {amount},<br>
        <u>Remarks from the business owner:</u> {remarks},<br>
        <u>Payment Link:</u> {link}<br><br>

        Thank You
        </p>
    </body>

    </html>
    '''
    message.attach(MIMEText(msg, 'html'))

    try:
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login("{}".format(os.getenv('TEST_EMAIL')), "{}".format(os.getenv('TEST_EMAIL_PASSWORD')))
            smtp.send_message(message)
            print("message sent successfully...")

    except:
        print("message was not...")


def generateLink(link):
    return 'http://127.0.0.1:5000'.join(link)