from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from icecream import ic
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from icecream import ic

model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")
ic(model)

# ic| model: SentenceTransformer(
# (0): Transformer({
    # 'max_seq_length': 512,
    # 'do_lower_case': False
    # }) with Transformer model: BertModel
# (1): Pooling({
    # 'word_embedding_dimension': 1024,
    # 'pooling_mode_cls_token': True,
    # 'pooling_mode_mean_tokens': False,
    # 'pooling_mode_max_tokens': False,
    # 'pooling_mode_mean_sqrt_len_tokens': False,
    # 'pooling_mode_weightedmean_tokens': False,
    # 'pooling_mode_lasttoken': False,
    # 'include_prompt': True
# })

# For retrieval you need to pass this prompt.
query = 'Represent this sentence for searching relevant passages: A man is eating a piece of bread'

pinecone_docs = [
    "the fifty mannequin heads floating in the pool kind of freaked them out",
    "she swore she just saw her sushi move",
    "he embraced his new life as an eggplant",
    "my dentist tells me that chewing bricks is very bad for your teeth",
    "the dental specialist recommended an immediate stop to flossing with construction materials",
]

# 2. Encode
embeddings = model.encode(pinecone_docs)
ic(embeddings)

sim = np.zeros((len(pinecone_docs), len(pinecone_docs)))
for i in range(len(pinecone_docs)):
    sim[i:,i] = cos_sim(embeddings[i], embeddings[i:])

df_sim = pd.DataFrame(sim, columns=[f'Doc {i+1}' for i in range(sim.shape[1])],
                      index=[f'Doc {i+1}' for i in range(sim.shape[0])])

# similarities = cos_sim(embeddings[0], embeddings[1:])
print('similarities:\n', sim)

# Show the DataFrame as a table
print("Similarity Table:")
print(df_sim)