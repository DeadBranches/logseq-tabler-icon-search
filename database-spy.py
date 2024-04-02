import json
from sqlite3 import connect
import numpy as np
from icecream import ic

ICON_DATAFILE = "icon_data.json"


def load_json(filepath):
    with open(filepath) as f:
        return json.load(f)


def main():
    ICON_DATAFILE = "icon_data.json"
    TABLE_NAME = "icons"
    TABLE_STRUCTURE = [
        ("name", "TEXT PRIMARY KEY"),
        ("tags", "TEXT"),
        ("category", "TEXT"),
        ("glyph", "TEXT"),
        ("vector", "TEXT"),
    ]
    KEYWORD_JOINER = ", "

    database_filename = TABLE_NAME + ".db"
    database = connect(database_filename)

    for row in database.execute(f"SELECT vector from {TABLE_NAME}"):
        binary_vector = row[0]
        icon_array = np.frombuffer(binary_vector, dtype=np.float32)
        ic(icon_array)

    database.close()


if __name__ == "__main__":
    main()
