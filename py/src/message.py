
import requests


def send_reminder_email(creds, mailing_list):
    print ('sending reminder email for %s' % mailing_list.game_id)
    subject = ""
    text = ""
    return requests.post(
        "https://api.mailgun.net/v3/%s/messages" % creds.mailgun_domain_name,
        auth=(
            "api",
            creds.mailgun_api_key,
        ),
        data={
            "from": "Cat Herder <robot@%s>" % creds.mailgun_domain_name,
            "to": mailing_list.contacts,
            "subject": subject,
            "text": text,
        },
    )
