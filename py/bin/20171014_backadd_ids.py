
import os
from py.src.store import (
    load_data,
    write_data,
)


def migrate_database():
    for f in os.listdir('local/db'):
        if '.json' in f:
            print('processing ' + f)
            game_id = (f.split('_')[1]).split('.')[0]
            week_id = f.split('_')[0]
            data = load_data(game_id, week_id)
            write_data(data)


if __name__ == "__main__":
    migrate_database()
