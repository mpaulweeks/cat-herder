
import json
import os

from py.src.model import (
    MailingList,
    EventWeek,
)

DATABASE_PATH = "local/database.json"
MAILING_LIST_PATH = "local/mailing_list.json"
MAILGUN_CREDENTIALS_PATH = "local/mailgun_credentials.json"


def load_mailgun_credentials():
    if not os.path.exists(MAILGUN_CREDENTIALS_PATH):
        raise Exception("no mailgun creds found")
    with open(MAILGUN_CREDENTIALS_PATH) as f:
        data = json.load(f)
    return [
        MailingList(key, val)
        for key, val in data.iteritems()
    ]


def load_mailing_lists():
    if not os.path.exists(MAILING_LIST_PATH):
        raise Exception("no mailing list found")
    with open(MAILING_LIST_PATH) as f:
        data = json.load(f)
    return [
        MailingList(key, val)
        for key, val in data.iteritems()
    ]


def load_data(game_id, week_id=None):
    """Loads the schelude for the requested week.

    Cat Herder only supports a single event per week, so `week_id` is a unique
    identifier for the schedule.

    """
    if not os.path.exists(DATABASE_PATH):
        with file(DATABASE_PATH, "w+") as f:
            f.write("{}")
    with open(DATABASE_PATH) as f:
        data = json.load(f)
    week_data = data.get(game_id, {}).get(week_id, {})
    return EventWeek.from_dict(game_id, week_id, week_data)


def write_data(week_data):
    with open(DATABASE_PATH) as f:
        file_data = json.load(f)
    game_data = file_data.get(week_data.game_id, {})
    game_data[week_data.id] = week_data.to_dict()
    file_data[week_data.game_id] = game_data
    with open(DATABASE_PATH, 'w') as f:
        json.dump(file_data, f)
