import pandas as pd
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

# 1. load model
model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")

# :param prompt_name: The name of the prompt to use for encoding. Must be a key in the prompts dictionary, which is either set in the constructor or loaded from the model configuration. For example if prompt_name is "query" and the prompts is {"query": "query: ", ...}, then the sentence "What is the capital of France?" will be encoded as "query: What is the capital of France?" because the sentence is appended to the prompt. If prompt is also set, this argument is ignored.
ICON_DATA = [
    {
        "name": "calendar-plus",
        "keywords": "calendar plus date day plan schedule agenda add calender",
        "category": "containing concept",
        "glyph": "ebba",
    },
    {
        "name": "calendar-minus",
        "keywords": "calendar minus date day plan schedule agenda calender",
        "category": "containing concept",
        "glyph": "ebb9",
    },
    {
        "name": "calendar-off",
        "keywords": "calendar off date day plan schedule agenda calender",
        "category": "containing concept",
        "glyph": "ee1f",
    },
    {
        "name": "circle-plus",
        "keywords": "circle plus add create new",
        "category": "correct",
        "glyph": "ea69",
    },
    {
        "name": "circle-minus",
        "keywords": "circle minus remove delete",
        "category": "correct",
        "glyph": "ea68",
    },
    {
        "name": "circle-half",
        "keywords": "circle half shape split slash",
        "category": "containing concept",
        "glyph": "ee3f",
    },
    {
        "name": "file-plus",
        "keywords": "file plus add create new",
        "category": "correct",
        "glyph": "eaa0",
    },
    {
        "name": "file-minus",
        "keywords": "file minus remove delete",
        "category": "correct",
        "glyph": "ea9e",
    },
    {
        "name": "exposure-plus-1",
        "keywords": "exposure plus 1 digit math number evaluation",
        "category": "containing concept",
        "glyph": "f29f",
    },
    {
        "name": "circle",
        "keywords": "circle false zero",
        "category": "containing concept",
        "glyph": "ea6b",
    },
    {
        "name": "alarm-plus-filled",
        "keywords": "alarm plus filled",
        "category": "containing concept",
        "glyph": "f70b",
    },
    {
        "name": "alarm-plus",
        "keywords": "alarm plus",
        "category": "containing concept",
        "glyph": "f631",
    },
    {
        "name": "calculator-off",
        "keywords": "calculator off math count add subtract multiply divide amount",
        "category": "related",
        "glyph": "f0c4",
    },
    {
        "name": "math-xy",
        "keywords": "math xy mathematic expression equation",
        "category": "related",
        "glyph": "f4f6",
    },
    {
        "name": "abacus-off",
        "keywords": "abacus off abacus math counting adding up",
        "category": "related",
        "glyph": "f3b6",
    },
    {
        "name": "abacus",
        "keywords": "abacus abacus math counting adding up",
        "category": "related",
        "glyph": "f05c",
    },
    {
        "name": "braces-off",
        "keywords": "braces off punctuation additional information",
        "category": "false friend",
        "glyph": "f0bf",
    },
    {
        "name": "layers-subtract",
        "keywords": "layers subtract stack",
        "category": "false friend",
        "glyph": "eaca",
    },
    {
        "name": "abc",
        "keywords": "abc letters alphabet latin",
        "category": "unrelated",
        "glyph": "f567",
    },
    {
        "name": "360-view",
        "keywords": "360 view degree rotation reality camera",
        "category": "unrelated",
        "glyph": "f566",
    },
    {
        "name": "3d-cube-sphere-off",
        "keywords": "3d cube sphere off printing vector shape",
        "category": "unrelated",
        "glyph": "f3b5",
    },
    {
        "name": "3d-cube-sphere",
        "keywords": "3d cube sphere printing vector shape",
        "category": "unrelated",
        "glyph": "ecd7",
    },
    {
        "name": "a-b-2",
        "keywords": "a b 2 test visual user",
        "category": "unrelated",
        "glyph": "f25f",
    },
    {
        "name": "a-b-off",
        "keywords": "a b off test visual user",
        "category": "unrelated",
        "glyph": "f0a6",
    },
    {
        "name": "123",
        "keywords": "123 numbers digit one two three",
        "category": "unrelated",
        "glyph": "f554",
    },
    {"name": "360", "keywords": "360", "category": "unrelated", "glyph": "f62f"},
    {
        "name": "24-hours",
        "keywords": "24 hours",
        "category": "unrelated",
        "glyph": "f5e7",
    },
]

PROMPTS = [
    "Represent this sentence for searching relevant passages: ",
    "Represent this keyword for searching relevant passages: ",
    "Represent this sentence for searching relevant keyword lists: ",
    "Represent this keyword for searching relevant keyword lists: ",
]
SENTENCES = ["addition", "subtraction", "wake"]


"""Returns a list containing every permutation of prompts + sentences.
E.g. [  'Represent this sentence for searching relevant passages: addition',
        'Represent this sentence for searching relevant passages: subtraction',
        ...]
"""
prompt_list = [prompt + sentence for prompt in PROMPTS for sentence in SENTENCES]

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

# similarities = cos_sim(embeddings[0], embeddings[1:])
# print("similarities:", similarities)


# >>> df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
# >>> df
#    col1  col2
# 0     1     3
# 1     2     4
# >>> df.T
#       0  1
# col1  1  2
# col2  3  4
df = pd.DataFrame(data=d)

from icecream import ic

ic(df)
df.to_csv("out.csv")
# document_list = [
#     "123 numbers digit one two three",
#     "360",
#     "24 hours",
#     "2fa login password verification code two-step",
#     "360 view degree rotation reality camera",
#     "3d cube sphere off printing vector shape",
#     "3d cube sphere printing vector shape",
#     "3d rotate rotation geometry 3d modeling",
#     "a b 2 test visual user",
#     "a b off test visual user",
#     "a b test visual user",
#     "abacus off abacus math counting adding up",
#     "abacus abacus math counting adding up",
#     "abc letters alphabet latin",
# ]
