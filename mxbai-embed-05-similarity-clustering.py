import json
from sqlite3 import connect
import numpy as np
from argparse import ArgumentParser

from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
from sentence_transformers.util import cos_sim


ICON_DATAFILE = "icon_data.json"


def load_json(filepath):
    with open(filepath) as f:
        return json.load(f)


def parse_cli_args():
    parser = ArgumentParser()
    parser.add_argument("query", help="The query string to search for")
    return parser.parse_args()


def load_icon_info_from_database(database, table_name):
    icon_info_list = []
    for row in database.execute(f"SELECT name, vector, glyph FROM {table_name}"):
        icon_info = {
            "name": row[0],
            "glyph": row[2],
            "vector": row[1],  # Keep the raw vector data
        }
        icon_info_list.append(icon_info)
    return icon_info_list


def compute_dbscan_clusters(similarity_scores):
    dbscan = DBSCAN(eps=0.1, min_samples=5)  # Adjust parameters as needed
    dbscan.fit(similarity_scores)
    return dbscan.labels_


def main():
    # Constants
    TOP_K = 5
    QUERY_PROMPT = "Represent this sentence for searching relevant passages: "
    ICON_DATAFILE = "icons_full.json"
    TABLE_NAME = "icons_full"

    # Load database
    database_filename = f"{TABLE_NAME}.db"
    database = connect(database_filename)

    # Get query from CLI arguments
    query = f"{QUERY_PROMPT} {parse_cli_args().query}"
    model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")
    query_embedding = model.encode(query)

    # Load icon information from the database
    icon_info_list = load_icon_info_from_database(database, TABLE_NAME)

    # Compute similarity scores for each icon
    similarity_scores = []
    for icon_info in icon_info_list:
        binary_vector = icon_info["vector"]
        icon_array = np.frombuffer(binary_vector, dtype=np.float32)
        similarity_score = cos_sim(query_embedding, icon_array)
        icon_info["similarity_score"] = similarity_score
        similarity_scores.append(similarity_score)

    # Compute DBSCAN clusters
    similarity_scores = np.array(similarity_scores).reshape(-1, 1)
    cluster_labels = compute_dbscan_clusters(similarity_scores)

    # Find the cluster label with the highest similarity score
    highest_similarity_cluster = np.argmax(similarity_scores)

    # Filter icons by cluster label
    relevant_icons = [
        info
        for i, info in enumerate(icon_info_list)
        if cluster_labels[i] == highest_similarity_cluster
    ]

    # Print the relevant icons
    for icon in relevant_icons:
        print(f"Icon Name: {icon['name']}, Glyph: {icon['glyph']}")

    # Close the database connection
    database.close()


if __name__ == "__main__":
    main()
