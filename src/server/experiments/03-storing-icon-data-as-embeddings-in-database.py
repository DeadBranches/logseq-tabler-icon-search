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
from typing import List, Dict, Set, Tuple, Any
from sqlite3 import Connection, connect, OperationalError, IntegrityError

from icecream import ic
from sentence_transformers import SentenceTransformer

## Configuration
DEBUG: bool = True  # Output info to console
# Filesystem-related
ICON_DATA_DIRECTORY: str = "icon-datafiles"
# ICONS_DATA_FILENAME = "tabler-icons-full.json"
ICONS_DATA_FILENAME: str = "tabler-icons-full.json"
DATABASE_DIRECTORY: str = "databases"
DATABASE_FILENAME_PREFIX: str = "mxbai-embed-09"  #
DATABASE_EXTENSTION: str = ".db"
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
EMBEDDING_MODEL: str = "mixedbread-ai/mxbai-embed-large-v1"
KEYWORD_JOINER: str = ", "  # I think semantically it makes sense to embed a list of
# keywords by sperating them with a comma. E.g. "circle, plus, add, create, new"
# Otherwise, space seperated keywords are a semantically gibberish sentence, right?
# E.g. "Circle plus add create new." has no meaning.

## Other constants
# Use the icon data filename as the database filename
database_filename: str = (
    DATABASE_FILENAME_PREFIX
    + "-"
    + os.path.splitext(ICONS_DATA_FILENAME)[0]
    + DATABASE_EXTENSTION
)
icon_data_file: str = os.path.join(ICON_DATA_DIRECTORY, ICONS_DATA_FILENAME)
# Use the icon data filename as the database filename
database_file: str = os.path.join(DATABASE_DIRECTORY, database_filename)


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

    def structure_icon_data(filepath: str) -> List[Dict]:
        icon_data: List[Dict] = load_json(filepath)  # ingest data
        processed_data: List[Dict] = []
        for item in icon_data:
            name: str = item["n"]
            keywords: str = item["t"]
            category: str = item["c"]
            glyph: str = item["u"]
            # Prevent duplicate keywords by using a set datatype, and include the icon
            # name in the embedding since it may contain useful information.
            keyword_set: Set = set(keywords.split(" "))
            keyword_set.add(name)
            # debug(keyword_set)
            # A comma seperated list is more semantically meaningful than space sperated.
            keyword_string: str = KEYWORD_JOINER.join(keyword_set)
            dict_entry = {
                "name": name,
                "keywords": keyword_string,
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
