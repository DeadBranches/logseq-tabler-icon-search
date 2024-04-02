import json

from icecream import ic

ICON_DATAFILE = "icon_data.json"


def load_json(filepath):
    with open(filepath) as f:
        return json.load(f)


icon_data = load_json(ICON_DATAFILE)

categories = set()

for icon in icon_data:
    categories.add(icon["c"])

ic(categories)
