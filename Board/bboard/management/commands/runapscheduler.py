import datetime
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.urls import reverse
from bboard.models import Post, Category, PostCategory

logger = logging.getLogger(__name__)



def my_job():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)

    posts = Post.objects.filter(date__gte=last_week)
    recipients = []
    for post in posts:
        for category in post.category.all():
            for subscriber in category.subscribers.all():
                recipients.append(subscriber.username)

    # Deduplicate recipients
    recipients = set(recipients)



    for recipient in recipients:
        subject = f"New Posts for the Week  of {last_week.strftime('%b %d, %Y')}"
        message = f"Hi {recipient},\n\nHere are the new posts for the week of {last_week.strftime('%b %d, %Y')}:\n\n"

        post_data = []

        for post in posts:
            post_url = reverse('bboard:post_detail', args=[str(post.id)])

            post_data.append({
                'title': post.title,
                'author': post.author,
                'url': post_url,
            })

        context = {
            'subject': subject,
            'message': message,
            'posts': post_data,
        }

        html_message = render_to_string('weekly_post.html', context)
        send_mail(subject, html_message, 'noreply@example.com', [recipients], fail_silently=False,
                  html_message=html_message)


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
