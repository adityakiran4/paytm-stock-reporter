import os
import requests
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from datetime import datetime

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

    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    text = soup.get_text(
        "\n",
        strip=True
    )

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    report_sections = []

    keywords = [
        "%",
        "Listed",
        "IPO",
        "Price"
    ]

    for i, line in enumerate(lines):

        if "%" in line:

            start = max(0, i - 8)
            end = min(len(lines), i + 3)

            section = "\n".join(
                lines[start:end]
            )

            report_sections.append(section)

    body = (
        "INDIA IPO REPORT\n"
        "========================\n\n"
        f"Generated: {datetime.now()}\n\n"
    )

    if report_sections:

        body += (
            "Recent IPO Listing Records\n"
            "-------------------------\n\n"
        )

        body += "\n\n=================================\n\n".join(
            report_sections[:20]
        )

    else:

        body += (
            "No IPO records found.\n"
            "Source page loaded successfully."
        )

    send_email(
        "India IPO Daily Report",
        body
    )


build_report()
