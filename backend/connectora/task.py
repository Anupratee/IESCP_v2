from workers import celery
from models import *
from mailer import send_email
from flask import render_template, send_file
from io import StringIO
import csv
from celery.schedules import crontab
from models import db, Request, Influencer, Sponsor, User

@celery.on_after_finalize.connect
def setup_periodic_task(sender, **kwargs):
    # sender.add_periodic_task(crontab(hour=10, minute=00), daily_reminder.s(), name="daily_reminder")
    #sender.add_periodic_task(30, daily_reminder.s(), name="daily_reminder")
    #sender.add_periodic_task(crontab(hour=10, minute=00, day_of_month="1"), monthly_report.s(), name="monthly_report")
    #sender.add_periodic_task(10, monthly_report.s(), name="monthly_report")
    sender.add_periodic_task(30, test.s(), name="test")


@celery.task
def send_task_email():
    html = render_template("daily_reminder.html")
    subject = "asdkljbasjkd"
    send_email("a@b.com", subject, html)
    return "sent email"


# @celery.task
# def daily_reminder():
#     requests = Request.query.all()
#     influencer_recipients = []
#     for request in requests:
#         if not request.influencer_id in influencer_recipients:
#             influencer_recipients.append(request.influencer_id)

#     subject = "Pending Requests"

#     for influencer in influencer_recipients:
#         user = User.query.get(influencer)
#         html = render_template("daily_reminder.html", user = user)
#         send_email(user.email, subject, html)


@celery.task
def monthly_report():
    receivers = ["meow@meow.com", "aa@aa.com"]
    subject = "monthly"

    for receiver in receivers:
        html = render_template("monthly_report.html")
        send_email(receiver, subject, html)


@celery.task
def test():
    return 1+2



def generate_csv():
    campaigns = [1, 2, 3]
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)

    csv_writer.writerow(["1", "2", "3"])

    for campaign in campaigns:
        csv_writer.writerow(["a", "b", "c"])

    return csv_buffer.getvalue()