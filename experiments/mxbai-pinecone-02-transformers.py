from typing import Dict

import torch
import numpy as np
from transformers import AutoModel, AutoTokenizer
from sentence_transformers.util import cos_sim
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from icecream import ic
import os


# For retrieval you need to pass this prompt. Please find our more in our blog post.
def transform_query(query: str) -> str:
    """For retrieval, add the prompt for query (not for documents)."""
    return f"Represent this sentence for searching relevant passages: {query}"


# The model works really well with cls pooling (default) but also with mean poolin.
def pooling(outputs: torch.Tensor, inputs: Dict, strategy: str = "cls") -> np.ndarray:
    if strategy == "cls":
        outputs = outputs[:, 0]
    elif strategy == "mean":
        outputs = torch.sum(
            outputs * inputs["attention_mask"][:, :, None], dim=1
        ) / torch.sum(inputs["attention_mask"])
    else:
        raise NotImplementedError
    return outputs.detach().cpu().numpy()


# 1. load model
model_id = "mixedbread-ai/mxbai-embed-large-v1"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModel.from_pretrained(model_id)

# pinecone_docs = [
#     "the fifty mannequin heads floating in the pool kind of freaked them out",
#     "she swore she just saw her sushi move",
#     "he embraced his new life as an eggplant",
#     "my dentist tells me that chewing bricks is very bad for your teeth",
#     "the dental specialist recommended an immediate stop to flossing with construction materials",
# ]
headers = ['math', 'calculator-off', 'calculator', 'math-x-plus-x', 'pencil-plus', 'layers', 'letter', 'list-search']
pinecone_docs = [
    "math, symbols, calculator, equal, plus, multiplication, minus, math",
"calculator-off, calculator, off, math, count, add, subtract, multiply, divide, amount",
"calculator, math, count, add, subtract, multiply, divide, amount",
"math-x-plus-x, math, x, plus, x, mathematic, expression, equation",
"pencil-plus, pencil, plus, add, edit, write, create, more",
"layers, subtract, stack",
"letter, n, alphabet, symbol, text, code",
"list-search, list, search, find, agenda, shopping",
]
# 2. encode
inputs = tokenizer(pinecone_docs, padding=True, return_tensors="pt")

for k, v in inputs.items():
    inputs[k] = v
outputs = model(**inputs).last_hidden_state
# embeddings = pooling(outputs, inputs, 'cls')
mean_embeddings = pooling(outputs, inputs, "mean")
cls_embeddings = pooling(outputs, inputs, "cls")


def create_matrix(docs, embeddings, labels):
    sim = np.zeros((len(docs), len(docs)))
    for i in range(len(docs)):
        sim[i:, i] = cos_sim(embeddings[i], embeddings[i:])
    # df_sim = pd.DataFrame(
    #     sim,
    #     columns=[f"Doc {i+1}" for i in range(sim.shape[1])],
    #     index=[f"Doc {i+1}" for i in range(sim.shape[0])],
    # )
    df_sim = pd.DataFrame(
        sim,
        columns=labels,
        index=labels,
    )
    return sim, df_sim

def truncate_string(text: str, truncate_at: int) -> str:
    """
    Truncate a string after a given number of characters and append '...'.

    Parameters:
    text (str): The string to be truncated.
    truncate_at (int): The number of characters at which to truncate the string.

    Returns:
    str: The truncated string with '...' appended if truncation occurs.
    """
    # Check if the length of the text is greater than the truncate_at value
    if len(text) > truncate_at:
        # Truncate the string and add '...'
        return text[:truncate_at] + '...'
    else:
        # Return the original text if no truncation is needed
        return text
    
def round_to_two_decimals(value):
    return round(value, 2)

# A list with each document truncated at 5 characters
truncated_docs = [truncate_string(doc, 5) for doc in pinecone_docs]

cls_matrix, cls_df = create_matrix(pinecone_docs, cls_embeddings, headers)
# print(cls_matrix, cls_df)
mean_matrix, mean_df = create_matrix(pinecone_docs, mean_embeddings, headers)
# print(mean_matrix, mean_df)


def mask_diagonal(df):
    mask = np.eye(len(df), dtype=bool)
    df_masked = df.mask(mask)
    return df_masked


def make_pretty(styler, truncate_at):
    # Define the truncate function with the given truncate_at parameter
    def truncate(v):
        return truncate_string(v, truncate_at)
    styler.set_caption("Similarity scores")
    # styler.format_index(truncate)
    styler.background_gradient()
    return styler

styles = [
    dict(selector="tr:hover",
                props=[("background", "#f4f4f4")]),
    dict(selector="th", props=[("color", "#fff"),
                               ("border", "1px solid #eee"),
                               ("padding", "12px 35px"),
                               ("border-collapse", "collapse"),
                               ("background", "#00cccc"),
                               ("text-transform", "uppercase"),
                               ("font-size", "18px")
                               ]),
    dict(selector="td", props=[("color", "#999"),
                               ("border", "1px solid #eee"),
                               ("padding", "12px 35px"),
                               ("border-collapse", "collapse"),
                               ("font-size", "15px")
                               ]),
    dict(selector="table", props=[
                                    ("font-family" , 'Arial'),
                                    ("margin" , "25px auto"),
                                    ("border-collapse" , "collapse"),
                                    ("border" , "1px solid #eee"),
                                    ("border-bottom" , "2px solid #00cccc"),                                    
                                      ]),
    dict(selector="caption", props=[("caption-side", "bottom")])
]
cls_df_masked = mask_diagonal(cls_df)
mean_df_masked = mask_diagonal(mean_df)
# Example usage:
mean_table = mean_df_masked.style \
    .format(precision=2, na_rep="") \
    .highlight_max() \
    .pipe(make_pretty, truncate_at=5) \
# .set_caption("Similarity scores") 
cls_table = cls_df_masked.style \
    .format(precision=2, na_rep="") \
    .highlight_max() \
    .pipe(make_pretty, truncate_at=5) \
# .set_caption("Similarity scores") 

# If the file already exists, overwrite it
mean_table_filename = "meantable.html"
if os.path.exists(mean_table_filename):
    os.remove(mean_table_filename)
mean_table.to_html(mean_table_filename)

cls_table_filename = "clstable.html"
if os.path.exists(cls_table_filename):
    os.remove(cls_table_filename)
cls_table.to_html(cls_table_filename)