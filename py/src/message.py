
import requests

from py.src.model import Calendar

# common helpers

ADMIN_EMAIL = "mpaulweeks@gmail.com"


def date_to_month_day(date_object):
    return date_object.strftime("%m/%d")


# weekly reminders

REMINDER_HTML = """https://cat-herder.mpaulweeks.com/%s/%s

To unsubscribe from this list, please email mpaulweeks@gmail.com
"""


def send_reminder_email(creds, mailing_list):
    next_week_name = date_to_month_day(Calendar.next_monday())
    next_week_id = Calendar.next_week_id()

    print ('sending reminder email for %s/%s' % (
        mailing_list.game.id, next_week_id
    ))

    subject = "%s %s" % (mailing_list.game.name, next_week_name)
    text = REMINDER_HTML % (
        mailing_list.game.id,
        next_week_id,
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
            "h:Reply-To": ADMIN_EMAIL,
        },
    )


# admin updates

UPDATE_HTML = """https://cat-herder.mpaulweeks.com/%s/%s

%s has %s"""


def send_update_email(creds, week, user_name, is_new):
    game = week.game
    week_name = date_to_month_day(week.date_object)

    print ('sending update email for %s/%s' % (
        game.id, week.id
    ))

    subject = "Update: %s %s" % (game.name, week_name)
    text = UPDATE_HTML % (
        game.id,
        week.id,
        user_name,
        'just added their RSVP' if is_new else 'updated their RSVP',
    )
    return requests.post(
        "https://api.mailgun.net/v3/%s/messages" % creds.mailgun_domain_name,
        auth=(
            "api",
            creds.mailgun_api_key,
        ),
        data={
            "from": "Cat Herder <cat.herder@%s>" % creds.mailgun_domain_name,
            "to": ADMIN_EMAIL,
            "subject": subject,
            "text": text,
            "h:Reply-To": ADMIN_EMAIL,
        },
    )
