
from datetime import (
    datetime,
    timedelta,
)
import time

from pytz import timezone


class Game(object):
    registry = {}
    registry_ids = []

    def __init__(self, id, name, subtitle, subject="???", hidden=False):
        self.id = id
        self.name = name
        self.subtitle = subtitle
        self.subject = subject
        self.hidden = hidden
        Game.register(self)

    @classmethod
    def register(cls, game):
        if game.id in cls.registry:
            raise Exception("game_id collision in registry")
        cls.registry[game.id] = game
        cls.registry_ids.append(game.id)

    @classmethod
    def get(cls, game_id):
        return cls.registry[game_id]

    @classmethod
    def get_all(cls):
        return cls.registry.values()

    @classmethod
    def contains(cls, game_id):
        return game_id in cls.registry

    @classmethod
    def next(cls, game_id):
        curr_index = cls.registry_ids.index(game_id)
        next_index = (curr_index + 1) % len(cls.registry_ids)
        next_id = cls.registry_ids[next_index]
        while cls.get(next_id).hidden:
            next_index = (next_index + 1) % len(cls.registry_ids)
            next_id = cls.registry_ids[next_index]
        return cls.get(next_id)


Game("edh", "Elder Dragon Highlander", "Usually hosted in Flatiron", subject="EDH @ Nielsen")
Game("smash", "Smash Ultimate", "Usually hosted in Gramercy", subject="Smash @ StuyTown", hidden=True)
Game("dominion", "Dominion", "Usually hosted at Zocdoc", hidden=True)
Game("ppstew", "Games with Stew", "Hosted somewhere at sometime", hidden=True)


class MailgunCredentials(object):
    def __init__(self, cred_dict):
        self.mailgun_api_key = cred_dict["mailgun_api_key"]
        self.mailgun_domain_name = cred_dict["mailgun_domain_name"]


class MailingList(object):
    def __init__(self, game_id, contacts):
        if not Game.contains(game_id):
            raise Exception("invalid game_id: %s", game_id)
        self.game = Game.get(game_id)
        self.contacts = contacts


class Calendar(object):
    @classmethod
    def from_str(cls, date_str):
        return datetime.strptime(date_str, '%Y%m%d')

    @classmethod
    def to_str(cls, date_object):
        return date_object.strftime('%Y%m%d')

    @classmethod
    def now(cls):
        eastern = timezone('US/Eastern')
        return datetime.now(eastern)

    @classmethod
    def this_monday(cls):
        local_time = cls.now()
        while local_time.weekday() != 0:  # 0 == Monday
            # walk back to find this Monday
            local_time = local_time - timedelta(days=1)
        return local_time

    @classmethod
    def last_week_id(cls, week_id):
        this_week = cls.from_str(week_id)
        return cls.to_str(this_week - timedelta(days=7))

    @classmethod
    def this_week_id(cls):
        return cls.to_str(cls.this_monday())

    @classmethod
    def next_monday(cls, week_id=None):
        this_week = cls.from_str(week_id or cls.this_week_id())
        return this_week + timedelta(days=7)

    @classmethod
    def next_week_id(cls, week_id=None):
        return cls.to_str(cls.next_monday(week_id))

    @classmethod
    def get_dates(cls, week_id):
        local_time = cls.from_str(week_id)
        dates = []
        for i in range(5):
            dates.append(EventDate(
                Calendar.to_str(local_time + timedelta(days=i)),
                ["6PM"],
            ))
        for i in range(5, 7):
            dates.append(EventDate(
                Calendar.to_str(local_time + timedelta(days=i)),
                ["12PM", "4PM"],
            ))
        return dates


class Participant(object):
    HIDDEN = 'style=display:none;'
    VISIBLE = ''

    @classmethod
    def random_id(cls):
        return str(int(time.time() * 1000000))

    def __init__(self, pid=None, name=None, availability=None):
        self.id = pid or self.random_id()
        self.name = name or ""
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
            p_data.get("i"),
            p_data["n"],
            p_data["a"],
        )

    def to_dict(self):
        return {
            "i": self.id,
            "n": self.name,
            "a": list(self.availability),
        }


class InvalidEventWeekStartException(Exception):
    pass


class EventWeek(object):
    def __init__(self, game_id, participants, event_dates, chosen, message):
        self.game = Game.get(game_id)
        self.participants = participants
        self.event_dates = event_dates
        min_date = min(self.event_dates, key=(lambda ed: ed.id))
        if min_date.dayName != "Monday":
            raise InvalidEventWeekStartException
        self.id = min_date.id
        self.date_object = min_date.date_object
        self.chosen = set()
        for event_id in chosen:
            self.toggle_chosen(event_id)
        self.message = message

    def upsert_participant(self, pid, new_name, events):
        to_edit = None
        for p in self.participants:
            if p.id == pid:
                to_edit = p
        is_new = not to_edit
        if not to_edit:
            to_edit = Participant(pid)
            self.participants.append(to_edit)
        to_edit.name = new_name
        to_edit.availability = set(events)
        return is_new

    def delete_participant(self, pid):
        self.participants = [
            p
            for p in self.participants
            if p.id != pid
        ]

    def toggle_chosen(self, event_id):
        event_domain = set(
            [et.event_id for ed in self.event_dates for et in ed.times]
        )
        if event_id not in event_domain:
            raise Exception

        if event_id in self.chosen:
            self.chosen.remove(event_id)
        else:
            self.chosen.add(event_id)

    @classmethod
    def from_dict(cls, game_id, week_id, w_data):
        p_datas = w_data.get("p", [])
        d_datas = w_data.get("d", [])
        participants = [Participant.from_dict(p_data) for p_data in p_datas]
        event_dates = [EventDate.from_dict(d_data) for d_data in d_datas]
        if not event_dates:
            event_dates = Calendar.get_dates(week_id)
        chosen = w_data.get("c", [])
        message = w_data.get("m", None)
        return EventWeek(game_id, participants, event_dates, chosen, message)

    def to_dict(self):
        return {
            "m": self.message,
            "p": [p.to_dict() for p in self.participants],
            "d": [d.to_dict() for d in self.event_dates],
            "c": list(self.chosen),
        }


class EventDate(object):
    def __init__(self, date_str, times):
        self.id = date_str
        self.times = [EventTime(self, t) for t in times]
        self.name = self.id[4:6] + "/" + self.id[6:]
        self.date_object = Calendar.from_str(date_str)
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

    def col_css(self, event_data):
        return " ".join([t.col_css(event_data) for t in self.times])


class EventTime(object):
    def __init__(self, event_date, time):
        self.event_date = event_date
        self.id = time
        self.event_id = event_date.id + time
        self.name = self.id

    def is_chosen(self, event_data):
        return self.event_id in event_data.chosen

    def col_css(self, event_data):
        return "col-" + self.event_id + (
            ' chosen' if self.is_chosen(event_data) else ''
        )

    def gcal(self, game):
        # mpwtodo hardcoded to 6-10pm
        utc_start_time = 180000
        duration = 40000

        dst_offset = 40000  # EDT during summer
        # dst_offset = 50000  # EDT during winter

        start_time = utc_start_time + dst_offset
        end_time = start_time + duration
        dates = "%sT%sZ/%sT%sZ" % (
            self.event_date.id, start_time, self.event_date.id, end_time
        )
        return (
            "http://www.google.com/calendar/event?action=TEMPLATE"
            "&dates=%s"
            "&text=%s"
            "&location=???"
            "&details=Hosted by:"
        ) % (dates, game.subject)
