import os
import yfinance as yf
import smtplib
from email.mime.text import MIMEText

# ==========================
# YOUR GMAIL SETTINGS
# ==========================



EMAIL = os.environ["EMAIL"]
APP_PASSWORD = os.environ["APP_PASSWORD"]
RECIPIENT = os.environ["RECIPIENT"]


# ==========================
# EMAIL FUNCTION
# ==========================

def send_email(subject, body):

    smtp = smtplib.SMTP("smtp.gmail.com", 587)

    smtp.ehlo()

    smtp.starttls()

    smtp.ehlo()

    smtp.login(EMAIL, APP_PASSWORD)

    msg = MIMEText(body, "plain", "utf-8")

    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = RECIPIENT

    smtp.send_message(msg)

    smtp.quit()

    print("Email Sent Successfully!")


# ==========================
# MORNING REPORT
# ==========================

def morning_report():

    ticker = yf.Ticker("PAYTM.NS")

    data = ticker.history(period="1d")

    open_price = data["Open"].iloc[-1]
    high_price = data["High"].iloc[-1]
    low_price = data["Low"].iloc[-1]
    close_price = data["Close"].iloc[-1]

    body = f"""
Good Morning!

PAYTM Daily Report

Open  : Rs. {open_price:.2f}
High  : Rs. {high_price:.2f}
Low   : Rs. {low_price:.2f}
Close : Rs. {close_price:.2f}

This report was generated automatically using Python.
"""

    send_email(
        "PAYTM Morning Report",
        body
    )


# ==========================
# RUN REPORT
# ==========================

morning_report()
