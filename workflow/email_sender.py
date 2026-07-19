import os
import smtplib

from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()


EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(receiver, subject, message):

    try:

        msg = MIMEText(message)

        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = receiver


        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()


        server.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )


        server.send_message(msg)

        server.quit()


        return True


    except Exception as e:

        print("Email Error:", e)

        return False