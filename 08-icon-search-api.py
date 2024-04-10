import json
import os
from typing import List, Dict, Set, Tuple, Any
from sqlite3 import Connection, connect, OperationalError, IntegrityError
from datetime import datetime
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
        parser.add_argument(
            "icon_keyword",
            help="Keyword(s) representing the tabler icons you want to find.",
        )
        return parser.parse_args()

    argument: str = parse_cli_args()

    def comma_seperate(keywords: str) -> str:
        """Convert space seperated words into comma seperated values"""
        keyword_set: Set = set(keywords.split(" "))
        return KEYWORD_JOINER.join(keyword_set)

    # search_string: str = comma_seperate(argument.icon_keyword)
    search_string: str = argument.icon_keyword

    def semantically_embed(model, text: str) -> List:
        """Generate a vector embedded with the semantictic meaning of the text."""
        text_embedding = model.encode(text)
        return text_embedding

    embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    search_query_embedding: List[str] = semantically_embed(
        embedding_model, f"{QUERY_PROMPT} {search_string}"
    )

    database: Connection = connect(database_file)

    icon_data = []
    for row in database.execute(f"SELECT name, vector, glyph from {TABLE_NAME}"):
        icon_label = row[0]
        icon_glyph = row[2]
        icon_keywords_embedding = np.frombuffer(row[1], dtype=np.float32)
        similarity_score = cos_sim(search_query_embedding, icon_keywords_embedding)
        icon_info = {
            "name": icon_label,
            "glyph": icon_glyph,
            "similarity_score": similarity_score,
        }
        icon_data.append(icon_info)
    database.close()

    sorted_icon_data = icon_data.copy()
    sorted_icon_data.sort(key=lambda x: x["similarity_score"], reverse=True)

    def get_top_k_results(icon_info_list, k):
        """Return the top k most similar icon results."""
        return icon_info_list[:k]

    top_k_results = get_top_k_results(icon_data, TOP_K)

    for icon in top_k_results:
        print(
            f"Icon Name: {icon['name']}, Glyph: {icon['glyph']}, Similarity Score: {icon['similarity_score']}"
        )

    def chart_probability_distribution(data, search_string) -> None:
        import seaborn as sns
        import matplotlib.pyplot as plt
        import random

        similarities = [float(d["similarity_score"].item()) for d in data]
        sns.histplot(similarities, kde=True)
        # Add a title and a subtitle to the plot
        plt.title("Distribution of Similarity Scores", y=1.01)
        plt.suptitle(f'Of icon keywords to "{search_string}"', fontsize="small")
        chart_filename = (
            f"distribution-{search_string}-{datetime.now().strftime('%M-%S')}.png"
        )
        plt.savefig(chart_filename, dpi=300)

    chart_probability_distribution(icon_data, search_string)


if __name__ == "__main__":
    main()
