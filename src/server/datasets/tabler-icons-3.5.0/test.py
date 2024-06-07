from icecream import ic

icon_data: dict[dict] = {
    "a-b-2": {
        "name": "a-b-2",
        "category": "",
        "tags": ["test", "visual", "user"],
        "styles": {"outline": {"version": "1.76", "unicode": "f25f"}},
    },
    "a-b-off": {
        "name": "a-b-off",
        "category": "",
        "tags": ["test", "visual", "user"],
        "styles": {"outline": {"version": "1.62", "unicode": "f0a6"}},
    },
}

KEYWORD_JOINER = ", "
processed_data: list[dict] = []

for item in icon_data.values():
    keywords_set: set = set()
    name: str = item["name"]
    category = item["category"]
    glyph: str = item["styles"]["outline"]["unicode"]
    keywords_set.add(name)
    for tag in item["tags"]:
        keywords_set.add(tag)
    keywords_string: str = KEYWORD_JOINER.join(keywords_set)
    dict_entry: dict = {
        "name": name,
        "keywords": keywords_string,
        "category": category,
        "glyph": glyph,
        "vector": "",
    }
    processed_data.append(dict_entry)
ic(processed_data)
