from celery import shared_task
from celery.utils.log import get_task_logger
# from celery.decorators import task
from django.conf import settings
from django.core.mail import EmailMessage,send_mail

# logger = get_task_logger(__name__)
# @task(name="send_notification_email")
@shared_task
def send_notification_email(emails,team):
    email_subject = f"You have been added to the team {team}"
    email_body = "Something"
    send_mail(
            subject=email_subject,
            message=email_body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails,
            fail_silently=True,
        )
    return "Done"
    # logger.info("sent notification mail")
    
    