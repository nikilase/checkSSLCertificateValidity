import requests
from datetime import datetime

from config.config import config
from tools.mailer import MailClient


def check_certsh():
    print("\nRunning crt.sh based check")
    base_url = "https://crt.sh/json?q="
    for cert in config.certs:
        cert_name = cert.name
        url = f"{base_url}{cert_name}&exclude=expired"
        result = requests.get(url)
        if result.status_code != 200:
            print(result.text)
            continue
        certs = result.json()

        # create our mailer object
        mail_client = MailClient(
            config.email_config.from_address,
            config.email_config.password,
            config.email_config.smtp_server,
            config.email_config.smtp_port,
        )

        # No active vert found
        if len(certs) == 0:
            mail_client.send_mail(
                config.email_config.to_email,
                f"WARNING: No active SSL Certificate found for {cert_name}!",
                f"Your SSL Certificate for {cert_name} Might be invalid already or nonexistant!\n"
                f"Please make sure to renew your certificate ASAP, or visitors to your website will encounter errors.",
                "plain",
                None,
                True,
            )
            continue

        latest = datetime.min
        for cert in certs:
            print(cert)
            cert_expires = datetime.strptime(cert["not_after"], "%Y-%m-%dT%H:%M:%S")
            if cert_expires > latest:
                latest = cert_expires

        print(f"Last Expiry: {latest}")
        days_to_expiration = (latest - datetime.now()).days
        print(days_to_expiration)

        # Send normal expiration info
        if days_to_expiration in [35, 28, 21, 14]:
            print(config.email_config.to_email)
            mail_client.send_mail(
                config.email_config.to_email,
                f"SSL Certificate {cert_name} expiring soon",
                f"Your SSL Certificate {cert_name} will expire in {days_to_expiration} days (on "
                f"{latest.date()}). \nPlease make sure to renew your certificate before then, or visitors to your "
                f"website will encounter errors.",
                "plain",
                None,
            )

        # Send critical expiration info
        if days_to_expiration <= 7:
            mail_client.send_mail(
                config.email_config.to_email,
                f"WARNING: SSL Certificate {cert_name} expiring really soon in {days_to_expiration} days!",
                f"Your SSL Certificate {cert_name} will expire really soon in only {days_to_expiration} days (on "
                f"{latest.date()}). \nPlease make sure to renew your certificate ASAP, or visitors to your website "
                f"will encounter errors.",
                "plain",
                None,
                True,
            )
