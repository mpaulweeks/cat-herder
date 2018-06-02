
import requests

from py.src.model import Calendar


REMINDER_HTML = """https://cat-herder.mpaulweeks.com/%s/%s

To unsubscribe from this list, please email mpaulweeks@gmail.com
"""


def send_reminder_email(creds, mailing_list):
    print ('sending reminder email for %s' % mailing_list.game.id)
    next_week = Calendar.next_monday().strftime("%m/%d")
    subject = "%s %s" % (mailing_list.game.name, next_week)
    text = REMINDER_HTML % (
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


UPDATE_HTML = """https://cat-herder.mpaulweeks.com/%s/%s

%s has %s"""


def send_update_email(creds, week, user_name, is_new):
    game = week.game
    print ('sending update email for %s' % game.id)
    subject = "Update: %s %s" % (game.name, Calendar.to_str(week.date_object))
    text = UPDATE_HTML % (
        game.id,
        week.id,
        user_name,
        'RSVPd' if is_new else 'updated their RSVP',
    )
    return requests.post(
        "https://api.mailgun.net/v3/%s/messages" % creds.mailgun_domain_name,
        auth=(
            "api",
            creds.mailgun_api_key,
        ),
        data={
            "from": "Cat Herder <cat.herder@%s>" % creds.mailgun_domain_name,
            "to": "mpaulweeks@gmail.com",
            "subject": subject,
            "text": text,
            "h:Reply-To": "mpaulweeks@gmail.com",
        },
    )
