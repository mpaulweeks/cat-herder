"""The Cat Herder server routing module.

"""

from datetime import datetime
import os

from py.src.bottle import (
    abort,
    delete,
    get,
    post,
    put,
    request,
    run,
    static_file,
    view,
)

from py.src.model import (
    Game,
    Calendar,
    Participant,
    InvalidEventWeekStartException,
)
from py.src.store import (
    load_data,
    write_data,
)

EPOCH = datetime.utcnow().strftime('%Y%m%d%H%M')
PROCESS_ID = os.getpid()


@get('/static/<filename>')
def static(filename):
    """Loads static files (e.g. CSS, Javascript).

    """
    return static_file(filename, root='static')


@get('/')
@view('directory')
def index():
    return {
        "epoch": EPOCH,
        "games": [
            game
            for game in Game.get_all()
            if not game.hidden
        ],
    }


def _game_view(game_id, week_id):
    if not Game.contains(game_id):
        abort(404, "No such event.")
    try:
        data = load_data(game_id, week_id)
    except InvalidEventWeekStartException:
        abort(400, "Start date must be a Monday")
    last_week_id = Calendar.last_week_id(week_id)
    next_week_id = Calendar.next_week_id(week_id)
    max_week_id = Calendar.next_week_id()
    return {
        "epoch": EPOCH,
        "data": data,
        "participants": data.participants + [Participant()],
        "today": Calendar.now(),
        "last_week_id": last_week_id if week_id > "20160808" else None,
        "next_week_id": next_week_id if next_week_id <= max_week_id else None,
        "next_game": Game.next(game_id),
    }


@get('/<game_id>')
@view('schedule')
def game(game_id):
    """Loads the main page.

    This loads the current state of the schedule from the database, and adds a
    new participant for the current user.
    """
    week_id = Calendar.this_week_id()
    return _game_view(game_id, week_id)


@get('/<game_id>/<week_id>')
@view('schedule')
def history(game_id, week_id):
    """Loads the main page.

    This loads the current state of the schedule from the database, and adds a
    new participant for the current user.
    """
    return _game_view(game_id, week_id)


def _update(request, game_id, week_id, pid):
    data = request.json
    new_participant_name = data['new_name']
    event_ids = data['event_ids']
    week_data = load_data(game_id, week_id)
    week_data.upsert_participant(
        pid,
        new_participant_name,
        event_ids,
    )
    write_data(week_data)
    return


@post('/game/<game_id>/event/<week_id>/participant')
def participant_post(game_id, week_id):
    return _update(request, game_id, week_id, None)


@put('/game/<game_id>/event/<week_id>/participant/<pid>')
def participant_put(game_id, week_id, pid):
    return _update(request, game_id, week_id, pid)


@delete('/game/<game_id>/event/<week_id>/participant/<pid>')
def delete(game_id, week_id, pid):
    week_data = load_data(game_id, week_id)
    week_data.delete_participant(pid)
    write_data(week_data)
    return


@put('/game/<game_id>/event/<week_id>/chosen/<event_id>')
def chosen(game_id, week_id, event_id):
    week_data = load_data(game_id, week_id)
    week_data.toggle_chosen(event_id)
    write_data(week_data)
    return


def run_server():
    with open('temp/server.pid', 'wt') as f:
        f.write(str(PROCESS_ID))
    run(
        host='localhost',
        port=5800,
        # debug=True,
    )
