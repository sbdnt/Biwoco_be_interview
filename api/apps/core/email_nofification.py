import boto3


from email import encoders
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



ses_client = boto3.client("ses", region_name="us-west-2")

def send_html_email():
    ses_client = boto3.client("ses", region_name="us-west-2")
    CHARSET = "UTF-8"
    HTML_EMAIL_CONTENT = """
        <html>
            <head></head>
            <h1 style='text-align:center'>This is the heading</h1>
            <p>Hello, world</p>
            </body>
        </html>
    """

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "noname@gmail.com",
            ],
        },
        Message={
            "Body": {
                "Html": {
                    "Charset": CHARSET,
                    "Data": HTML_EMAIL_CONTENT,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Amazing Email Tutorial",
            },
        },
        Source="noname@gmail.com",
    )


def send_email_with_attachment():
    msg = MIMEMultipart()
    msg["Subject"] = "This is an email with an attachment!"
    msg["From"] = "noname@gmail.com"
    msg["To"] = "noname@gmail.com"

    # Set message body
    body = MIMEText("Hello, world!", "plain")
    msg.attach(body)

    filename = "document.pdf"  # In same directory as script

    with open(filename, "rb") as attachment:
        part = MIMEApplication(attachment.read())
        part.add_header("Content-Disposition",
                        "attachment",
                        filename=filename)
    msg.attach(part)

    # Convert message to string and send
    ses_client = boto3.client("ses", region_name="us-west-2")
    response = ses_client.send_raw_email(
        Source="abhishek@learnaws.org",
        Destinations=["abhishek@learnaws.org"],
        RawMessage={"Data": msg.as_string()}
    )


def create_custom_verification_email_template():
    ses_client = boto3.client('ses')
    response = ses_client.create_custom_verification_email_template(
        TemplateName= "CustomVerificationTemplate",
        FromEmailAddress= "abhishek@learnaws.org",
        TemplateSubject= "Please confirm your email address",
        TemplateContent= """
            <html>
            <head></head>
            <h1 style='text-align:center'>Please verify your account</h1>
            <p>Before we can let you access our product, please verify your email</p>
            </body>
            </html>
        """,
        SuccessRedirectionURL= "https://yourdomain.com/success",
        FailureRedirectionURL= "https://yourdomain.com/fail"
    )
