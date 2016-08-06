
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
    HIDDEN = 'style=display:none;'
    VISIBLE = ''

    def __init__(self, name=None, availability=None):
        self.name = name
        self.availability = set(availability or [])

    @property
    def is_old(self):
        return self.VISIBLE if self.name else self.HIDDEN

    @property
    def is_new(self):
        return self.HIDDEN if self.name else self.VISIBLE

    @property
    def clickable(self):
        return '' if self.name else 'clickable'

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
            "a": list(self.availability),
        }


class EventWeek(object):
    def __init__(self, participants, event_dates):
        self.participants = participants
        self.event_dates = event_dates
        min_date = min(self.event_dates, key=(lambda ed: ed.id))
        self.id = min_date.id
        self.date_object = min_date.date_object

    def upsert_participant(self, old_name, new_name, events):
        to_edit = None
        for p in self.participants:
            if p.name == old_name:
                to_edit = p
        if not to_edit:
            to_edit = Participant(old_name)
            self.participants.append(to_edit)
        to_edit.name = new_name
        to_edit.availability = set(events)

    def delete_participant(self, name):
        self.participants = [
            p
            for p in self.participants
            if p.name != name
        ]

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
        self.date_object = datetime.strptime(date_str, '%Y%m%d')
        self.dayName = self.date_object.strftime('%A')

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
