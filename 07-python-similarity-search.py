import json
import os
from typing import List, Dict, Set, Tuple, Any
from sqlite3 import Connection, connect, OperationalError, IntegrityError

from argparse import ArgumentParser

import numpy as np
from icecream import ic
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

## Configuration
DEBUG: bool = True  # Output info to console
# Filesystem-related
ICON_DATA_DIRECTORY: str = "icon-datafiles"
# ICONS_DATA_FILENAME = "tabler-icons-full.json"
ICONS_DATA_FILENAME: str = "tabler-icons-full.json"
DATABASE_DIRECTORY: str = "databases"
DATABASE_FILENAME_PREFIX: str = "mxbai-embed-06"  #
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
TOP_K = 5
QUERY_PROMPT = "Represent this sentence for searching relevant passages:"


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


def main():
    debug(f"icon data file: {icon_data_file}\ndatabase file: {database_file}")

    def parse_cli_args():
        parser = ArgumentParser()
        parser.add_argument("icon_keyword", help="The query string to search for")
        return parser.parse_args()

    argument: str = parse_cli_args()

    def comma_seperate(keywords: str) -> str:
        """Convert space seperated keywords into comma seperated values"""
        keyword_set: Set = set(keywords.split(" "))
        return KEYWORD_JOINER.join(keyword_set)

    search_query: str = comma_seperate(argument.icon_keyword)
    debug(search_query)

    def semantically_embed(model, keyword: str) -> List:
        """Generate a semantic text embedding vector"""
        vector_embedding = model.encode(f"{QUERY_PROMPT} {keyword}")
        return vector_embedding

    embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    query_embedding: List[str] = semantically_embed(embedding_model, search_query)

    database: Connection = connect(database_file)

    icon_info_list = []

    for row in database.execute(f"SELECT name, vector, glyph from {TABLE_NAME}"):
        binary_vector = row[1]
        icon_array = np.frombuffer(binary_vector, dtype=np.float32)
        similarity_score = cos_sim(query_embedding, icon_array)
        icon_info = {
            "name": row[0],
            "glyph": row[2],
            "similarity_score": similarity_score,
        }
        icon_info_list.append(icon_info)

    icon_info_list.sort(key=lambda x: x["similarity_score"], reverse=True)

    # Function to get top k similar results
    def get_top_k_results(icon_info_list, k):
        """Return the top k most similar icon results."""
        return icon_info_list[:k]

    # Get the top k results
    top_k = 5  # Set the value of k to your preference
    top_k_results = get_top_k_results(icon_info_list, top_k)

    # Print the top k results
    for icon in top_k_results:
        print(
            f"Icon Name: {icon['name']}, Glyph: {icon['glyph']}, Similarity Score: {icon['similarity_score']}"
        )

    database.close()


if __name__ == "__main__":
    main()
