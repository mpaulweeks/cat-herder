
from bottle import (
    Bottle,
    abort,
    get,
    response,
    request,
    run,
    template,
    view,
    static_file,
)


def getDates():
    from datetime import datetime, timedelta
    from pytz import timezone
    eastern = timezone('US/Eastern')
    local_time = datetime.now(eastern)
    while local_time.weekday() != 0:  # 0 == Monday
        local_time = local_time + timedelta(days=1)
    for i in range(5):
        yield EventDate(
            local_time + timedelta(days=i),
            ["6PM"],
        )
    for i in range(5, 7):
        yield EventDate(
            local_time + timedelta(days=i),
            ["12PM", "4PM"],
        )


class Person(object):

    def __init__(self, name):
        self.name = name
        self.availability = set()

    def get(self, event_time):
        return event_time.key in self.availability


class EventDate(object):

    def __init__(self, date, times):
        self.date = date
        self.key = date.strftime('%Y%m%d')
        self.times = [EventTime(self, t) for t in times]


class EventTime(object):

    def __init__(self, event_date, time):
        self.event_date = event_date
        self.time = time
        self.key = event_date.key + time


@get('/static/<filename>')
def static(filename):
    return static_file(filename, root='static')


@get('/')
@view('index')
def index():
    dates = list(getDates())
    return {
        "dates": dates,
        "people": [Person("Mike")],
    }

run(
    host='localhost',
    port=5800,
    debug=True,
)
