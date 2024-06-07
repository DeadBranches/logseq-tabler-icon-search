""" Implements:
        - Data ingestion and processing over a logseq tabler-icon json file.
        - Semantic vector embeddings over keyword lists.
        - Database creation and data insertion operations. 
    Creates standards for:
        - Data and database file and folder names/locations
        - Logical operation structures
    TODO: Convert hardcoded values in add_to_database() to @dataclasses
"""

import json
import os
import sys
from sqlite3 import Connection, IntegrityError, OperationalError, connect
from typing import Any, Dict, List, Set, Tuple

from icecream import ic
from sentence_transformers import SentenceTransformer

## Configuration
DEBUG: bool = True  # Output info to console

EMBEDDING_MODEL: str = "mixedbread-ai/mxbai-embed-large-v1"
# Filesystem-related
ICON_DATA_DIRECTORY: str = "datasets/tabler-icons-3.5.0"
# ICONS_DATA_FILENAME = "tabler-icons-full.json"
ICONS_DATA_FILENAME: str = "icons.json"
DATABASE_DIRECTORY: str = "datasets/tabler-icons-3.5.0"
DATABASE_EXTENSION: str = "sqlite3"
# Database configuration
TABLE_NAME: str = "icons"
TABLE_STRUCTURE: List[Tuple] = [
    ("name", "TEXT PRIMARY KEY"),
    ("tags", "TEXT"),
    ("category", "TEXT"),
    ("glyph", "TEXT"),
    ("vector", "TEXT"),
]
# Embeddings config
KEYWORD_JOINER: str = ", "  # I think semantically it makes sense to embed a list of
# keywords by sperating them with a comma. E.g. "circle, plus, add, create, new"
# Otherwise, space seperated keywords are a semantically gibberish sentence, right?
# E.g. "Circle plus add create new." has no meaning.

## Other constants
# Use the icon data filename as the database filename
model_name: str = EMBEDDING_MODEL.split("/")[1]  # used in the database name
icon_data_basename = os.path.splitext(ICONS_DATA_FILENAME)[0]
database_filename: str = f"{icon_data_basename}-{model_name}.{DATABASE_EXTENSION}"

icon_data_file: str = os.path.join(
    sys.path[0], ICON_DATA_DIRECTORY, ICONS_DATA_FILENAME
)
# Use the icon data filename as the database filename
database_file: str = os.path.join(sys.path[0], DATABASE_DIRECTORY, database_filename)


# Helpers
def debug(content: Any) -> None:
    """Print arguments to the console."""
    if DEBUG:
        data_type = type(content)
        ic(data_type, content)


def load_json(file_path: str) -> List | Dict:
    with open(file_path, "r") as f:
        return json.load(f)


def main():
    debug(f"icon data file: {icon_data_file}\ndatabase file: {database_file}")

    database: Connection = connect(database_file)
    embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    ic(type(embedding_model))

    def initialize_database(
        db_connection: Connection, table_name: str, table_structure: List[Tuple]
    ):
        """Initialize the database by attempting to create the table.
        If the table already exists, this will do nothing."""
        try:
            # SQL expects columns as `name type, name type...`
            # But TABLE_STRUCTURE is [(name, type), (name, type) ...]
            table_columns = []
            for name, type in table_structure:
                table_columns.append(f"{name} {type}")
            column_definition = ", ".join(table_columns)
            db_connection.execute(f"CREATE TABLE {table_name}({column_definition})")
            debug(f"Table '{table_name} created")
        except OperationalError as e:
            debug(e)

    initialize_database(database, TABLE_NAME, TABLE_STRUCTURE)

    # Structure of json file is:
    dummy_data = {
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

    def structure_icon_data(filepath: str) -> List[Dict]:
        icon_data: List[Dict] = load_json(filepath)  # ingest data
        processed_data: List[Dict] = []
        for item in icon_data.values():
            name: str = item["name"]
            category = item["category"]
            glyph: str = item["styles"]["outline"]["unicode"]

            keywords_set: Set[str] = set()
            # Sometimes the keywords list already includes the icon name
            keywords_set.add(name)
            for keyword in item["tags"]:
                if keyword is not None:
                    keywords_set.add(str(keyword))

            keywords_string: str = KEYWORD_JOINER.join(keywords_set)
            dict_entry: dict = {
                "name": name,
                "keywords": keywords_string,
                "category": category,
                "glyph": glyph,
                "vector": "",
            }
            processed_data.append(dict_entry)
        return processed_data

    icons_data = structure_icon_data(icon_data_file)

    def generate_keyword_embeddings(model, icons_data: List[Dict]):
        """Given a list of icon entries with a keyword key, create a list of
        vector embeddings for each keyword."""
        keyword_embeddings: List = []
        for icon in icons_data:
            embedding_text = icon["keywords"]
            ic(embedding_text)
            vector_embedding = model.encode(embedding_text)
            keyword_embeddings.append(vector_embedding)
        return keyword_embeddings

    keyword_embeddings: List = generate_keyword_embeddings(embedding_model, icons_data)

    # Create a copy of icon_data that maps vectors to the vector key
    icons_and_embeddings: List[Dict] = []
    for i, icon in enumerate(icons_data):
        icon["vector"] = keyword_embeddings[i]
        icons_and_embeddings.append(icon)
    ic(icons_and_embeddings)

    def add_to_database(db_connection: Connection, icons_and_embeddings):
        with db_connection:
            for icon in icons_and_embeddings:
                try:
                    db_connection.execute(
                        f"INSERT INTO {TABLE_NAME} VALUES (?, ?, ?, ?, ?)",
                        (
                            icon["name"],
                            icon["keywords"],
                            icon["category"],
                            icon["glyph"],
                            icon["vector"],
                        ),
                    )
                except IntegrityError as error:
                    debug(error)
                    debug(f"Skipping {icon['name']} due to duplicate entry.")
                    continue

    add_to_database(database, icons_and_embeddings)

    # Prove that the inset worked by printing the number of rows in the table
    row_count = database.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]
    debug(row_count)

    database.close()


if __name__ == "__main__":

    main()
