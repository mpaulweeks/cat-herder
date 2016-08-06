"""The Cat Herder server routing module.

"""

import json
import os

from bottle import (
    delete,
    get,
    put,
    request,
    run,
    static_file,
    view,
)

from model import (
    EventWeek,
    Participant,
)

DATABASE_PATH = "database.json"


def load_data(week_id=None):
    """Loads the schelude for the requested week.

    Cat Herder only supports a single event per week, so `week_id` is a unique
    identifier for the schedule.

    """
    if not os.path.exists(DATABASE_PATH):
        with file(DATABASE_PATH, "w+") as f:
            f.write("{}")
    with open(DATABASE_PATH) as f:
        data = json.load(f)
    week_data = data.get(week_id, {})
    return EventWeek.from_dict(week_data)


def write_data(week_data):
    with open(DATABASE_PATH) as f:
        file_data = json.load(f)
    file_data[week_data.id] = week_data.to_dict()
    with open(DATABASE_PATH, 'w') as f:
        json.dump(file_data, f)


@get('/static/<filename>')
def static(filename):
    """Loads static files (e.g. CSS, Javascript).

    """
    return static_file(filename, root='static')


@get('/')
@view('index')
def index():
    """Loads the main page.

    This loads the current state of the schedule from the database, and adds a
    new participant for the current user.
    """
    data = load_data("20160808")
    print data.to_dict()
    return {
        "data": data,
        "participants": data.participants + [Participant()],
    }


@put('/event/<week_id>/participant/<old_participant_name>')
def update(week_id, old_participant_name):
    data = request.json
    print data
    new_participant_name = data['new_name']
    event_ids = data['event_ids']
    week_data = load_data(week_id)
    week_data.upsert_participant(
        old_participant_name,
        new_participant_name,
        event_ids,
    )
    write_data(week_data)
    return


@delete('/event/<week_id>/participant/<participant_name>')
def delete(week_id, participant_name):
    week_data = load_data(week_id)
    week_data.delete_participant(participant_name)
    write_data(week_data)
    return

run(
    host='localhost',
    port=5800,
    debug=True,
)
