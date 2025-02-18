import json
import socket
import ssl
import datetime

from tools.mailer import MailClient
from config.config import config


def check_hostname(hostname: str, port: int):
    # Get the respective certificate
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            certificate = ssock.getpeercert()

    # Extract the certificate name and expiration date
    print(f"Found Certificate: {certificate}")
    certificate_name = certificate["subject"][0][0][1]
    cert_expires = datetime.datetime.strptime(
        certificate["notAfter"], "%b %d %H:%M:%S %Y %Z"
    )
    days_to_expiration = (cert_expires - datetime.datetime.now()).days
    print(f"Valid for {days_to_expiration} days")

    # create our mailer object
    mail_client = MailClient(
        config.email_config.from_address,
        config.email_config.password,
        config.email_config.smtp_server,
        config.email_config.smtp_port,
    )

    # Send normal expiration info
    if days_to_expiration in [35, 28, 21, 14]:
        print(config.email_config.to_email)
        mail_client.send_mail(
            config.email_config.to_email,
            f"SSL Certificate {certificate_name} expiring soon",
            f"Your SSL Certificate {certificate_name} will expire in {days_to_expiration} days (on "
            f"{cert_expires.date()}). \nPlease make sure to renew your certificate before then, or visitors to your "
            f"website will encounter errors.",
            "plain",
            None,
        )

    # Send critical expiration info
    if days_to_expiration <= 7:
        mail_client.send_mail(
            config.email_config.to_email,
            f"WARNING: SSL Certificate {certificate_name} expiring really soon in {days_to_expiration} days!",
            f"Your SSL Certificate {certificate_name} will expire really soon in only {days_to_expiration} days (on "
            f"{cert_expires.date()}). \nPlease make sure to renew your certificate ASAP, or visitors to your website "
            f"will encounter errors.",
            "plain",
            None,
            True,
        )


def runner():
    print("\nRunning Hostname based check")
    for host in config.hosts:
        check_hostname(host.url, host.port)


if __name__ == "__main__":
    runner()
