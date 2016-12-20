
import requests

from py.src.model import Calendar


def send_reminder_email(creds, mailing_list):
    print ('sending reminder email for %s' % mailing_list.game.id)
    next_week = Calendar.next_monday().strftime("%m/%d")
    subject = "%s %s" % (mailing_list.game.name, next_week)
    text = "http://cat-herder.mpaulweeks.com/%s/%s" % (
        mailing_list.game.id,
        Calendar.next_week_id(),
    )
    return requests.post(
        "https://api.mailgun.net/v3/%s/messages" % creds.mailgun_domain_name,
        auth=(
            "api",
            creds.mailgun_api_key,
        ),
        data={
            "from": "Cat Herder <cat.herder@%s>" % creds.mailgun_domain_name,
            "to": mailing_list.contacts,
            "subject": subject,
            "text": text,
            "h:Reply-To": "mpaulweeks@gmail.com",
        },
    )
