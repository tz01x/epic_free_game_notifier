from datetime import datetime
import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os,pytz
from typing import List
from epicbot_interface.models import Subscribers
from epicbot_interface.epic_bot.utils import get_date_obj

def notify_all_subs():

    sub_users = Subscribers.objects.filter(
       is_active=True)

    notify_sub_user(sub_users)
    print("send email to ",sub_users.count())


def notify_sub_user(subs_users):
    """
    send email to Subscribers
    """
    with open("epicbot_interface/epic_bot/previously_seen_product.json", "r", encoding="utf-8") as f:
        previously_seen_game: dict = json.load(f)

    items = [
        value for _, value in previously_seen_game.items()
        if not (
            datetime.now().astimezone(tz=pytz.UTC)
            > get_date_obj(value["promotionalOffers_end_date"]).astimezone(tz=pytz.UTC)
        )
    ]
    full_text = f"""\
    Dear Subscribers,
    We are excited to announce that Epic Games is offering free copy of {', '.join((item['title'] for item in items))} on the Epic Store.
    To claim your free game, simply visit the Epic Store and log in with your Epic Games account. The game will be added to your library automatically. This offer is only available for a limited time, so don't miss out on this opportunity to try out this exciting new game.
    Thank you for your continued support. We hope you enjoy the game!
    Sincerely,
    epicBot
    """
    html_p1 =f"""\
    <html>
    <body>
        <p>Dear Subscribers,</p>
        <p>We are excited to announce that Epic Games is offering free copy of <strong>{', '.join((item['title'] for item in items))}</strong> on the Epic Store.</p>
    """     
    html_p2 = ''
    for item in items:
        html_p2 += f"""
        <div>
            <div >
                
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                <tr>
                    <td width="33%" align="center" valign="top" style="font-family:Arial, Helvetica, sans-serif; font-size:2px; color:#ffffff;">.</td>
                    <td width="35%" align="center" valign="top">
                    <img src="{item['image_url']}" style="max-width:400px" atr="game cover">

                    </td>
                    <td width="33%" align="center" valign="top" style="font-family:Arial, Helvetica, sans-serif; font-size:2px; color:#ffffff;">.</td>
                </tr>
                </table>
            </div>
            <div style="border-left: 5px solid #cbcbcb;padding-left: 10px;">
                <p style="text-align: center;"><strong>{item['title']}</strong></p>
                <p><i>{item['description']}</i></p>
                <div> 
                    <strong>
                        Expired Date: {get_date_obj(item['promotionalOffers_end_date']).astimezone(tz=pytz.UTC).strftime("%H:%M:%S at %Y-%m-%d")}
                    </strong>
                </div>
                <div>
                <p>
                    To claim this game, click on this <a href="https://store.epicgames.com/en-US/p/{item['productSlug']}">link</a>
                </p>
                </div>
            </div>
        </div>
        <hr/>
        """
    html_p3="""
    <p>To claim your free game(s),simply visit the Epic Store and log in with your Epic Games account.
        This offer is only available for a limited time, 
        so don't miss out on this opportunity to try out this exciting new game.</p>
        <p>Thank you for your continued support. We hope you enjoy the game!</p>
        <p>Sincerely,<br>
        <strong>epicBot</strong>
    </p>
    """
    for user in subs_users:
        send_mail(full_text,html_p1+html_p2+html_p3, user)


def send_mail(full_text,html, user):
    sender_email = os.getenv('EMAIL',default='abcd')
    password = os.getenv('PASS',default='abcd')

    message = MIMEMultipart("alternative")
    message["Subject"] = f"Free Game - on Epic Store (Limited Time Offer)"

    html = f"""\
        {html}
        <div style="text-align: center">
        <small> <a href="https://ebot01y.pythonanywhere.com/unsubscribe/?id={user.id}">unsubscribe</a>  </small>
        </div>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(full_text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, user.email, message.as_string())
