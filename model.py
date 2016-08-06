
from datetime import (
    datetime,
    timedelta,
)

from pytz import timezone


def getDates():
    eastern = timezone('US/Eastern')
    local_time = datetime.now(eastern)
    while local_time.weekday() != 0:  # 0 == Monday
        local_time = local_time + timedelta(days=1)
    for i in range(5):
        yield EventDate(
            (local_time + timedelta(days=i)).strftime('%Y%m%d'),
            ["6PM"],
        )
    for i in range(5, 7):
        yield EventDate(
            (local_time + timedelta(days=i)).strftime('%Y%m%d'),
            ["12PM", "4PM"],
        )


class Participant(object):
    def __init__(self, name=None):
        self.name = name
        self.availability = set()

    def get(self, event_time):
        return event_time.event_id in self.availability

    @classmethod
    def from_dict(cls, p_data):
        return Participant(
            p_data["n"],
            p_data["a"],
        )

    def to_dict(self):
        return {
            "n": self.name,
            "a": self.availability,
        }


class EventWeek(object):
    def __init__(self, participants, event_dates):
        self.participants = participants
        self.event_dates = event_dates
        self.id = min(self.event_dates, key=(lambda ed: ed.id)).id

    @classmethod
    def from_dict(cls, w_data):
        p_datas = w_data.get("p", [])
        d_datas = w_data.get("d", [])
        participants = [Participant.from_dict(p_data) for p_data in p_datas]
        event_dates = [EventDate.from_dict(d_data) for d_data in d_datas]
        if not event_dates:
            event_dates = list(getDates())
        return EventWeek(participants, event_dates)

    def to_dict(self):
        return {
            "p": [p.to_dict() for p in self.participants],
            "d": [d.to_dict() for d in self.event_dates],
        }


class EventDate(object):
    def __init__(self, date_str, times):
        self.id = date_str
        self.times = [EventTime(self, t) for t in times]
        self.name = self.id[4:6] + "/" + self.id[6:]

    @classmethod
    def from_dict(cls, d_data):
        id = d_data["id"]
        times = d_data["t"]
        return EventDate(id, times)

    def to_dict(self):
        return {
            "id": self.id,
            "t": [t.id for t in self.times],
        }


class EventTime(object):
    def __init__(self, event_date, time):
        self.event_date = event_date
        self.id = time
        self.event_id = event_date.id + time
        self.name = self.id
