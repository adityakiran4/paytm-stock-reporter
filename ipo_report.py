import os
import smtplib
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


def ipo_report():

    ipo_listings = [
        ("Antala Industries", "11-Nov-2026"),
        ("Vedant Poly Fabs", "09-Nov-2026"),
        ("Johnsoncab Electricals", "06-Nov-2026"),
        ("HGS India", "06-Nov-2026"),
        ("Maxwell Engineering Solutions", "06-Nov-2026"),
        ("Vectras Enprocon", "06-Nov-2026")
    ]

    body = "COMPANIES LISTED IN LAST 10 DAYS\n\n"

    for company, listing_date in ipo_listings:
        body += f"{company} - {listing_date}\n"

    body += f"\nGenerated on: {datetime.now().strftime('%d-%b-%Y %H:%M')}"

    send_email(
        "IPO Listings - Last 10 Days",
        body
    )


ipo_report()
