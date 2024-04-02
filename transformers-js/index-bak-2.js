import { pipeline, cos_sim } from '@xenova/transformers';
// const sqlite3 = require('sqlite3').verbose();
import sqlite3 from 'sqlite3';

// Configuration options
const ICON_DATAFILE = 'icon_data.json';
const DATABASE_FILENAME = 'icons_partial.db';
const TABLE_NAME = 'icons';
const QUERY_PROMPT = 'Represent this sentence for searching relevant passages: addition';

const sqlSelect = `SELECT name, vector, glyph FROM ${TABLE_NAME}`;

async function main() {

    // Load existing icon database from file
    const db = new sqlite3.Database(DATABASE_FILENAME, sqlite3.OPEN_READONLY);

    // Create a list to hold icon info
    const iconInfoList = [];
    await db.all(sqlSelect, [], (err, rows) => {
        if (err) {
            console.error(err.message);
            return;
        }
        rows.forEach((row) => {
            // Fetch the vector and generate a similarity score
            const binaryVector = Buffer.from(row.vector, 'base64');
            const vector = new Float32Array(binaryVector.buffer);
            const similarityScore = cos_sim([[0.11], [0.12]], [[0.01], [0.12]]);

            const iconInfo = {
                name: row.name,
                glyph: row.glyph,
                similarityScore,
            };
            // Debug: print the content of IconInfo to console
            console.log(iconInfo); // { name: 'plus', glyph: 'plus', similarityScore: 0.9999999 }
            iconInfoList.push(iconInfo);
        }, () => {
            console.log(iconInfoList); // [{ name: 'plus', glyph: 'plus', similarityScore: 0.9999999 }, { name: 'plus-circle', glyph: 'plus-circle', similarityScore: 0.9999999 }]
            db.close();

        });
    });
}

main();
// // Create a feature extraction pipeline
// const extractor = await pipeline('feature-extraction', 'mixedbread-ai/mxbai-embed-large-v1', {
//     quantized: false, // Comment out this line to use the quantized version
// });

// // Generate sentence embeddings
// const docs = [
//     'Represent this sentence for searching relevant passages: A man is eating a piece of bread',
//     'A man is eating food.',
//     'A man is eating pasta.',
//     'The girl is carrying a baby.',
//     'A man is riding a horse.',
// ]
// const output = await extractor(docs, { pooling: 'cls' });

// // Compute similarity scores
// const [source_embeddings, ...document_embeddings ] = output.tolist();
// const similarities = document_embeddings.map(x => cos_sim(source_embeddings, x));
// console.log(similarities); // [0.7919578577247139, 0.6369278664248345, 0.16512018371357193, 0.3620778366720027]
