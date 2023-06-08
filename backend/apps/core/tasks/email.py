from celery import shared_task
from templated_mail.mail import BaseEmailMessage
from decouple import config
from config.celery import celery


@celery.task
def send_email(
    template_path: str,
    to_email: str,
    subject: str,
    context: dict
) -> None:
    '''Send email in the background using Celery'''

    # Do not send emails while testing
    if config('TESTING', default=False, cast=bool):
        return

    # Create an email message using the provided template and context
    email_message = BaseEmailMessage(
        subject=subject,
        template_name=template_path,
        context={**context},
    )

    # Send the email to the specified recipient
    email_message.send(to=[to_email])
