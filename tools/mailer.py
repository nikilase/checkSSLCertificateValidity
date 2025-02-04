import smtplib
from dataclasses import dataclass
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


@dataclass
class EmailAttachment:
    name: str
    data: bytes


class MailClient:
    def __init__(
        self, from_address: str, password: str, smtp_server: str, smtp_port: int
    ):
        self.from_address = from_address
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def test_mail(self, recipient: list[str]):
        # Create the HTML version of your message
        html = """
                <html>
                <body>
                <p>Hi,<br>
                This is a test email.<br>
                -Python
                </p>
                </body>
                </html>
                """
        self.send_mail(recipient, "Automated Email", html, "html")

    def send_mail(
        self,
        recipient: list[str],
        subject: str,
        body: str,
        body_type: str,
        attachments: list[EmailAttachment] | None = None,
        important: bool = False,
    ):
        """
        Send an email via the no reply email.

        :param important: Set the important flag in the mail
        :param recipient: Recipient or list of recipients
        :param subject: Subject text
        :param body: Can be html string or plaintext
        :param body_type: Either "html" or "plain"
        :param attachments: Optional List of Attachments
        """
        # Adding a newline before the body text fixes the missing message body
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.from_address
        msg["To"] = ", ".join(recipient)
        if important:
            msg["X-Priority"] = "1"  # Mark as important
            msg["X-MSMail-Priority"] = "High"  # Mark as high priority for Outlook

        # Turn these into plain/html MIMEText objects
        part = MIMEText(body, body_type)

        # Add HTML/plain-text parts to MIMEMultipart message
        msg.attach(part)

        if attachments:
            for attachment in attachments:
                part = MIMEApplication(attachment.data)
                part.add_header(
                    "Content-Disposition", "attachment", filename=attachment.name
                )
                msg.attach(part)

        mailserver = smtplib.SMTP(self.smtp_server, self.smtp_port)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.login(self.from_address, self.password)
        mailserver.sendmail(self.from_address, recipient, msg.as_string())
        mailserver.quit()
