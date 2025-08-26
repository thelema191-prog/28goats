import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
EMAIL_FROM = os.environ.get("EMAIL_FROM") or EMAIL_USER
EMAIL_TO = os.environ.get("EMAIL_TO") or EMAIL_USER

def send_email(to_addr: str, subject: str, html_body: str):
    if not EMAIL_HOST or not EMAIL_USER or not EMAIL_PASS:
        return False
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = to_addr
    part_html = MIMEText(html_body, "html")
    msg.attach(part_html)
    ctx = ssl.create_default_context()
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls(context=ctx)
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_FROM, [to_addr], msg.as_string())
    return True

def notify_owner(subject: str, html: str):
    to = os.environ.get("EMAIL_TO") or EMAIL_FROM
    return send_email(to, subject, html)

def wrap_email(title: str, body: str):
    return f"""<div><h2>{title}</h2><div>{body}</div></div>"""
