from celery import shared_task
from templated_mail.mail import BaseEmailMessage
from decouple import config


@shared_task
def send_email(template_path: str, to_email: str, subject: str, context: dict) -> None:
    """
    Send email to the specified recipient using the provided template and context.
    """

    # The default domain for sending links in html message
    context.update({"default_domain": config("DEFAULT_DOMAIN")})

    # Create an email message using the provided template and context
    email_message = BaseEmailMessage(
        subject=subject,
        template_name=template_path,
        context={**context},
    )

    # Send the email to the specified recipient
    email_message.send(to=[to_email])
