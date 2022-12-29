from datetime import datetime
import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from epicbot_interface.models import Subscribers
from epicbot_interface.epic_bot.utils import get_date_obj


def send_email_to_all_user(title, description):
    """
    send email to Subscribers
    """

    receiver_emails = Subscribers.objects.filter(
       is_active=True).values_list('email', flat=True)

    for remail in receiver_emails:
        send_mail(title, description, remail)


def get_active_promo_game():

    with open("epicbot_interface/epic_bot/previously_seen_product.json", "r", encoding="utf-8") as f:
        previously_seen_game: dict = json.load(f)

    for k, value in previously_seen_game.items():
        # if current time is grater then promo end time
        if (
            datetime.utcnow()
            > get_date_obj(value["promotionalOffers_end_date"]).utcnow()
        ):
            continue

        # notify user
        send_email_to_all_user(value["title"], value["description"])





def send_mail(title, description, receiver_email):
    sender_email = os.getenv('EMAIL',default='abcd')
    password = os.getenv('PASS',default='abcd')

    message = MIMEMultipart("alternative")
    message["Subject"] = f"Free Game - {title} on Epic Store (Limited Time Offer)"

    # Create the plain-text and HTML version of your message
    text = f"""\
    Dear Subscribers,
    We are excited to announce that Epic Games is offering free copy of {title} on the Epic Store.
    {description}
    To claim your free game, simply visit the Epic Store and log in with your Epic Games account. The game will be added to your library automatically. This offer is only available for a limited time, so don't miss out on this opportunity to try out this exciting new game.
    Thank you for your continued support. We hope you enjoy the game!
    Sincerely,
    epicBot
    """
    html = f"""\
    <html>
    <body>
        <p>Dear Subscribers,</p>
        <p>We are excited to announce that Epic Games is offering free copy of <strong>{title}</strong> on the Epic Store.</p>
        <p><i>{description}</i></p>
        <p>To claim your free game, simply visit the Epic Store and log in with your Epic Games account.
        The game will be added to your library automatically. This offer is only available for a limited time, 
        so don't miss out on this opportunity to try out this exciting new game.</p>
        <p>Thank you for your continued support. We hope you enjoy the game!</p>
        <p>Sincerely,<br>
        <strong>epicBot</strong>
        </p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
