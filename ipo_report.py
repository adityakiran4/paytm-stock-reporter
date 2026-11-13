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

    text = soup.get_text("\n", strip=True)

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    report_rows = []

    for i, line in enumerate(lines):

        if "%" in line and "+" in line:

            try:

                company = lines[i - 5]
                list_date = lines[i - 4]
                ipo_price = lines[i - 3]
                listing_price = lines[i - 2]
                gain = lines[i]

                report_rows.append(
                    (
                        company[:30],
                        list_date[:12],
                        ipo_price,
                        listing_price,
                        gain
                    )
                )

            except IndexError:
                pass

    body = []
    body.append("INDIA IPO REPORT")
    body.append("=" * 80)
    body.append("")
    body.append(
        f"Generated: {datetime.now().strftime('%d-%b-%Y %H:%M')}"
    )
    body.append("")

    body.append(
        f"{'COMPANY':30} | {'DATE':12} | {'IPO':10} | {'LISTING':10} | GAIN"
    )

    body.append("-" * 80)

    for row in report_rows[:25]:

        body.append(
            f"{row[0]:30} | "
            f"{row[1]:12} | "
            f"{row[2]:10} | "
            f"{row[3]:10} | "
            f"{row[4]}"
        )

    send_email(
        "India IPO Report",
        "\n".join(body)
    )


build_report()
