
from py.src.store import (
    load_mailgun_credentials,
    load_mailing_lists,
)
from py.src.message import (
    send_reminder_email,
)


def send_emails():
    creds = load_mailgun_credentials()
    for mlist in load_mailing_lists():
        # print mlist.__dict__
        send_reminder_email(creds, mlist)

if __name__ == "__main__":
    send_emails()
