
import json

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


def load_data(week_id=None):
    with open("database.json") as f:
        data = json.load(f)
    week_data = data.get(week_id, {})
    return EventWeek.from_dict(week_data)


@get('/static/<filename>')
def static(filename):
    return static_file(filename, root='static')


@get('/')
@view('index')
def index():
    data = load_data()
    print data.to_dict()
    return {
        "data": data,
        "participants": data.participants + [Participant()],
    }


@put('/update')
def update():
    data = request.forms.get('data')
    print data
    return

run(
    host='localhost',
    port=5800,
    debug=True,
)
