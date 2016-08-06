"""The Cat Herder server routing module.

"""

import json
import os

from bottle import (
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
        with file(DATABASE_PATH, "w+") as database:
            database.write("{}")
    with open(DATABASE_PATH) as database:
        data = json.load(database)
    week_data = data.get(week_id, {})
    return EventWeek.from_dict(week_data)


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
    data = load_data()
    print data.to_dict()
    return {
        "data": data,
        "participants": data.participants + [Participant()],
    }


@put('/event/<week_id>/participant/<participant_name>')
def update(week_id, participant_name):
    data = request.json
    print data
    return

run(
    host='localhost',
    port=5800,
    debug=True,
)
