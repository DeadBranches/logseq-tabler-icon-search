from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from icecream import ic

# 1. load model
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

docs = [
    query,
    "A man is eating food.",
    "A man is eating pasta.",
    "The girl is carrying a baby.",
    "A man is riding a horse.",
]

# 2. Encode
embeddings = model.encode(docs)

similarities = cos_sim(embeddings[0], embeddings[1:])
print('similarities:', similarities)
