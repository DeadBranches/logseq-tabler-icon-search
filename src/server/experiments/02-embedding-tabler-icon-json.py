import pandas as pd
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from icecream import ic

# 1. load model
model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")

# :param prompt_name: The name of the prompt to use for encoding. Must be a key in the prompts dictionary, which is either set in the constructor or loaded from the model configuration. For example if prompt_name is "query" and the prompts is {"query": "query: ", ...}, then the sentence "What is the capital of France?" will be encoded as "query: What is the capital of France?" because the sentence is appended to the prompt. If prompt is also set, this argument is ignored.
ICON_DATA = [
    {
        "name": "calendar-plus-comma",
        "keywords": "calendar, plus, date, day, plan, schedule, agenda, add, calender",
        "category": "containing concept",
        "glyph": "ebba",
    },
    {
        "name": "calendar-plus-space",
        "keywords": "calendar plus date day plan schedule agenda add calender",
        "category": "containing concept",
        "glyph": "ebba",
    },
    {
        "name": "calendar-plus-period",
        "keywords": "calendar. plus. date. day. plan. schedule. agenda. add. calender",
        "category": "containing concept",
        "glyph": "ebba",
    },
]


PROMPTS = [
    "Represent this sentence for searching relevant passages: ",
]
SENTENCES = ["addition", "subtraction", "wake"]


"""Returns a list containing every permutation of prompts + sentences.
E.g. [  'Represent this sentence for searching relevant passages: addition',
        'Represent this sentence for searching relevant passages: subtraction',
        ...]
"""
prompt_list = [prompt + sentence for prompt in PROMPTS for sentence in SENTENCES]

# Keyword permutations
# Build a number of different type of keyword permutations
# a) comma seperated b) space seperated c) period seperated
keyword_seperator_label = ["comma seperated", "space seperated", "period seperated"]
keyword_seperator = [", ", " ", ". "]

# We're just generating text embeddings for an icon's keywords
icon_keywords = [
    item["keywords"] for item in ICON_DATA
]  # ['circle plus add create new', 'circle minus remove delete' ...]
icon_names = [item["name"] for item in ICON_DATA]  # ['circle-plus', 'circle-minus' ...]


query_embedding = model.encode(prompt_list)
keyword_embedding = model.encode(icon_keywords)

# Each list item in icon_keywords is a column in a pandas dataframe, represented by a key having the name of icon_names[item index].
# And each dataframe row represents a cosine similarity score between the icon keyword text embedding and query_embeddings[n]. And each row is a list item
# E.g. df = {"calendar-plus": [[0.11, 0.123 ...], [0.1, 0.2], ...], "calendar-minus": [[...] ...]}

# For each item in icon_names, we're calculating the cosine similarity between the keyword text embedding (with the same index as icon_name) and each query_embedding
d = {}
d["prompts"] = prompt_list
for i, icon_name in enumerate(icon_names):
    similarity_score_list = []
    for embedding in query_embedding:
        similarity_score = cos_sim(keyword_embedding[i], embedding)
        similarity_score_list.append(similarity_score)
    d[icon_name] = similarity_score_list


df = pd.DataFrame(data=d)


ic(df)
