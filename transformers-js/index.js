import { pipeline, cos_sim } from '@xenova/transformers';
// const sqlite3 = require('sqlite3').verbose();
import sqlite3 from 'sqlite3';

// Configuration options
const ICON_DATAFILE = 'icon_data.json';
const DATABASE_FILENAME = 'icons_full.db';
const TABLE_NAME = 'icons_full';
const QUERY_PROMPT = `Represent this sentence for searching relevant passages: ${process.argv[2]}`;

const sqlSelect = `SELECT name, vector, glyph FROM ${TABLE_NAME}`;

// Load existing icon database from file
const db = new sqlite3.Database(DATABASE_FILENAME, sqlite3.OPEN_READONLY);

// Create a list to hold icon info

// Callback function for handling database results
function handleDatabaseResults(err, rows) {
    if (err) {
        console.error(err.message);
        return;
    }
    const iconInfoList = [];
    for (const row of rows) {
        const binaryVector = Buffer.from(row.vector, 'base64');
        const vector = new Float32Array(binaryVector.buffer);
        const iconInfo = {
            name: row.name,
            glyph: row.glyph,
            vector: vector,
        };
        // console.log(iconInfo);
        iconInfoList.push(iconInfo);
    }
    return iconInfoList;
}

function queryDatabase() {
    return new Promise((resolve, reject) => {
        db.all(sqlSelect, [], (err, rows) => {
            if (err) {
                reject(err);
            } else {
                resolve(handleDatabaseResults(null, rows));
            }

        });
    });
}
async function main() {
    try {

        const iconInfoList = await queryDatabase();
        // console.log(iconInfoList);

        const extractor = await pipeline('feature-extraction', 'mixedbread-ai/mxbai-embed-large-v1', {
            quantized: false, // Comment out this line to use the quantized version
        });
        const query_vector = await extractor(QUERY_PROMPT, { pooling: 'cls' });
        // console.log(query_vector);

        // console.log("iconInfoList\n")
        // console.log(iconInfoList);
        // console.log("query_vector\n")
        // console.log(query_vector);

        // Create a new list of dictionaries by iterating over iconInfoList and adding name, glyph, and a calculated similarity score
        const newIconInfoList = [];
        for (const iconInfo of iconInfoList) {
            const similarity = cos_sim(query_vector.data, iconInfo.vector);
            const newIconInfo = {
                name: iconInfo.name,
                glyph: iconInfo.glyph,
                similarity: similarity,
            };
            newIconInfoList.push(newIconInfo);
        }
        // Sort the newIconInfoList by similarity score in descending order
        newIconInfoList.sort((a, b) => b.similarity - a.similarity);
        // Show the top 10 results ordered by highest similarity score
        // console.log("newIconInfoList\n")
        // console.log(newIconInfoList);
        // console.log("newIconInfoList.slice(0, 10)\n");
        // Store the top 10 results in a variable called top10
        console.log(newIconInfoList.slice(0, 10));
        const top10 = newIconInfoList.slice(0, 10);
        //For each result in the top 10 print the icon name, the hex code converted to a unicode glyph, and the similarity score
        for (const result of top10) {
            const unicodeValue = parseInt(result.glyph, 16);
            // const glyph = String.fromCodePoint(unicodeValue);
            const glyph = String.fromCharCode(unicodeValue);
            console.log(`${result.name} ${glyph} ${result.similarity}`); 
        }
    } catch (err) {
        console.error(err);
    }
}
        

main();
// var iconInfoList = [];
// console.log(iconInfoList);

// // Create a feature extraction pipeline


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
