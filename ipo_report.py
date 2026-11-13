import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import smtplib
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


def get_recent_ipos():

    url = "https://www.motilaloswal.com/ipos"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    html = requests.get(
        url,
        headers=headers,
        timeout=30
    ).text

    soup = BeautifulSoup(html, "html.parser")

    text = soup.get_text("\n")

    lines = [
        x.strip()
        for x in text.split("\n")
        if x.strip()
    ]

    records = []

    for i, line in enumerate(lines):

        if "Listed date" in line:

            try:

                company = lines[i - 1]

                listing_date = line.replace(
                    "Listed date", ""
                ).strip()

                listing_price = ""

                gain = ""

                for j in range(i, min(i + 5, len(lines))):

                    if "₹" in lines[j]:
                        listing_price = lines[j]

                    if "%" in lines[j]:
                        gain = lines[j]

                records.append({
                    "Company": company,
                    "Listing Date": listing_date,
                    "Price": listing_price,
                    "Gain": gain
                })

            except:
                pass

    return records


def create_report():

    records = get_recent_ipos()

    body = (
        "INDIA IPO LISTINGS REPORT\n"
        "Last 10 Days\n\n"
    )

    for row in records:

        body += (
            f"{row['Company']}\n"
            f"Listing Date : {row['Listing Date']}\n"
            f"Listing Price: {row['Price']}\n"
            f"Listing Gain : {row['Gain']}\n\n"
        )

    body += (
        f"\nGenerated: "
        f"{datetime.now()}"
    )

    send_email(
        "India IPO Listings Report",
        body
    )


create_report()
