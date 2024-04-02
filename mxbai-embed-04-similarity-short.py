import json
from sqlite3 import connect
import numpy as np
from argparse import ArgumentParser
from icecream import ic

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from sklearn.cluster import DBSCAN

ICON_DATAFILE = "icon_data.json"


def load_json(filepath):
    with open(filepath) as f:
        return json.load(f)


def parse_cli_args():
    parser = ArgumentParser()
    parser.add_argument("query", help="The query string to search for")
    return parser.parse_args()


def main():
    # ICON_DATAFILE = "icon_data.json"
    TOP_K = 5
    QUERY_PROMPT = "Represent this sentence for searching relevant passages: "
    ICON_DATAFILE = "icons_full.json"
    TABLE_NAME = "icons_full"
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

    query = f"{QUERY_PROMPT} {parse_cli_args().query}"
    model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")
    query_embedding = model.encode(query)

    icon_info_list = []

    for row in database.execute(f"SELECT name, vector, glyph from {TABLE_NAME}"):
        binary_vector = row[1]
        icon_array = np.frombuffer(binary_vector, dtype=np.float32)
        similarity_score = cos_sim(query_embedding, icon_array)
        # ic(f"{row[0]}: {similarity_score}")

        # Store icon information in a dictionary
        icon_info = {
            "name": row[0],
            "glyph": row[2],
            "similarity_score": similarity_score,
        }
        icon_info_list.append(icon_info)

    similarity_scores = [info["similarity_score"] for info in icon_info_list]
    similarity_scores = np.array(similarity_scores).reshape(-1, 1)

    dbscan = DBSCAN(eps=0.1, min_samples=5)  # Adjust parameters as needed
    dbscan.fit(similarity_scores)

    # Get cluster labels for each similarity score
    cluster_labels = dbscan.labels_

    # Determine the adaptive threshold
    threshold = np.percentile(
        similarity_scores, 90
    )  # Example: Top 10% similarity scores

    # # Create a dictionary to store clusters
    # clusters = {}  # {cluster_label: [icon_info1, icon_info2, ...]}

    # # Group icons into clusters
    # for i, icon_info in enumerate(icon_info_list):
    #     cluster_label = cluster_labels[i]
    #     if cluster_label not in clusters:
    #         clusters[cluster_label] = []
    #     clusters[cluster_label].append(icon_info)

    # # Print all icons within each cluster
    # for cluster_label, icons in clusters.items():
    #     ic(f"Cluster {cluster_label}:")
    #     for icon in icons:
    #         ic(icon)
    # Find the cluster label with the highest similarity score
    highest_similarity_cluster = np.argmax(similarity_scores)

    # Filter icons by cluster label
    relevant_icons = [
        icon_info
        for i, icon_info in enumerate(icon_info_list)
        if cluster_labels[i] == highest_similarity_cluster
    ]

    # Print the relevant icons
    for icon in relevant_icons:
        ic(icon)

    # Print the cluster labels and threshold
    ic("Cluster labels:", cluster_labels)
    ic("Adaptive threshold:", threshold)

    # Sort the list based on similarity scores (higher scores first)
    icon_info_list.sort(key=lambda x: x["similarity_score"], reverse=True)

    # Retrieve the top-k similar results
    top_k_results = icon_info_list[:TOP_K]

    # Print the top-k results
    for result in top_k_results:
        ic(result)

    database.close()


if __name__ == "__main__":
    main()
