
const fs = require('fs');
const sqlite3 = require('sqlite3').verbose();
// const { pipeline, cos_sim } = require('@xenova/transformers');
const ICON_DATAFILE = 'icon_data.json';
const TOP_K = 5;
const QUERY_PROMPT = 'Represent this sentence for searching relevant passages:';
const ICON_DATAFILE_JS = 'icons_full.json';
const TABLE_NAME = 'icons_full';



async function loadJson(filepath) {
    const data = await fs.promises.readFile(filepath, 'utf-8');
    return JSON.parse(data);
}

async function main() {
    try {
        const query = process.argv[2];
        const { pipeline, cos_sim } = await import('@xenova/transformers'); // Dynamic import

        const model = await pipeline('feature-extraction', 'mixedbread-ai/mxbai-embed-large-v1', {
            quantized: false, // Comment out this line to use the quantized version
        });

        const queryEmbedding = await model.encodeSentences([`${QUERY_PROMPT} ${query}`], { pooling: 'cls' });
        const db = new sqlite3.Database(`${TABLE_NAME}.db`);

        const iconInfoList = [];
        db.each(`SELECT name, vector, glyph FROM ${TABLE_NAME}`, (err, row) => {
            if (err) {
                console.error(err.message);
                return;
            }
            const binaryVector = Buffer.from(row.vector, 'base64');
            const iconArray = new Float32Array(binaryVector.buffer);
            const similarityScore = cos_sim(queryEmbedding, iconArray);

            // Store icon information in an object
            const iconInfo = {
                name: row.name,
                glyph: row.glyph,
                similarityScore,
            };
            iconInfoList.push(iconInfo);
        }, () => {
            // Sort the list based on similarity scores (higher scores first)
            iconInfoList.sort((a, b) => b.similarityScore - a.similarityScore);

            // Retrieve the top-k similar results
            const topKResults = iconInfoList.slice(0, TOP_K);

            // Print the top-k results
            console.log(topKResults);
            db.close();
        });
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main();