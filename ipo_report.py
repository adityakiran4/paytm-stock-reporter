import os
import requests
import pandas as pd
import smtplib
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from email.mime.text import MIMEText

EMAIL = os.environ["EMAIL"]
APP_PASSWORD = os.environ["APP_PASSWORD"]
RECIPIENT = os.environ["RECIPIENT"]


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


def build_report():

    url = "https://www.ipomarket.in/ipo/listed"

    html = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    ).text

    body = (
        "INDIA IPO REPORT\n"
        "===================\n\n"
    )

    keywords = [
        "Listed Date",
        "Listing Price",
        "Listing Gain"
    ]

    found = []

    for line in html.splitlines():

        for keyword in keywords:

            if keyword in line:

                found.append(line.strip())

    body += (
        f"Page downloaded successfully.\n\n"
        f"Keyword matches found: {len(found)}\n\n"
    )

    body += "\n".join(found[:100])

    body += (
        f"\n\nGenerated: "
        f"{datetime.now()}"
    )

    send_email(
        "IPO Report Test",
        body
    )


build_report()
