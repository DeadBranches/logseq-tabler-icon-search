import { pipeline, cos_sim } from '@xenova/transformers';

// Create a feature extraction pipeline
const extractor = await pipeline('feature-extraction', 'mixedbread-ai/mxbai-embed-large-v1', {
    quantized: false, // Comment out this line to use the quantized version
});

// Generate sentence embeddings
const query = "Represent this sentence for searching relevant passages: A man is eating a piece of bread";
const doc = "A man is eating food";

const query_vector = await extractor(query, { pooling: 'cls' });
const doc_vector = await extractor(doc, { pooling: 'cls' });
console.log(query_vector); 
console.log(doc_vector); 
const similarity = cos_sim(query_vector.data, doc_vector.data);
console.log(similarity);
