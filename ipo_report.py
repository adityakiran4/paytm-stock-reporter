import os
import smtplib
from email.mime.text import MIMEText
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

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


def fetch_page():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        page.goto(
            "https://www.motilaloswal.com/ipos",
            wait_until="networkidle",
            timeout=60000,
        )

        page.wait_for_timeout(5000)

        html = page.content()

        browser.close()

        return html


def create_report():

    html = fetch_page()

    soup = BeautifulSoup(html, "html.parser")

    body = f"""
TITLE:
{soup.title.text}

URL THAT LOADED:
https://www.motilaloswal.com/ipos
"""

    send_email(
        "IPO PAGE DEBUG",
        body
    )


create_report()
