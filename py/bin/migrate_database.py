
import json

from py.src.store import (
    get_database_path,
)


def migrate_database():
    with open("local/database.json") as f:
        data = json.load(f)
    for game_id, game_data in data.iteritems():
        for week_id, week_data in game_data.iteritems():
            with file(get_database_path(week_id, game_id), "w+") as f:
                file_data = {game_id: {week_id: week_data}}
                json.dump(file_data, f)


if __name__ == "__main__":
    migrate_database()
