from icecream import ic
from sentence_transformers import CrossEncoder, SentenceTransformer
from sentence_transformers.util import cos_sim

rerank_model = CrossEncoder("mixedbread-ai/mxbai-rerank-base-v1")

icon_results_one = {
    "result": [
        {
            "name": "analyze-off",
            "glyph": "f3ba",
            "keywords": "data, analyze, analytics, graph, off, analyze-off, statistics",
            "similarity_score": 0.6050139665603638,
        },
    ]
}
icon_results = {
    "result": [
        {
            "name": "analyze-off",
            "glyph": "f3ba",
            "keywords": "data, analyze, analytics, graph, off, analyze-off, statistics",
            "similarity_score": 0.6050139665603638,
        },
        {
            "name": "function-off",
            "glyph": "f3f0",
            "keywords": "statyscics, linear, math, off, function, graph, function-off",
            "similarity_score": 0.5888403654098511,
        },
        {
            "name": "graph-off",
            "glyph": "f3f4",
            "keywords": "chart, raport, analytics, graph-off, graph, off, statistics",
            "similarity_score": 0.5826255679130554,
        },
        {
            "name": "chart-arrows",
            "glyph": "ee2a",
            "keywords": "variable, arrows, decrease, data, chart, level, statistical, value, increase, scale, chart-arrows, statistics",
            "similarity_score": 0.5798454880714417,
        },
        {
            "name": "brain",
            "glyph": "f59f",
            "keywords": "mind, brain, organ, human, iq, inteligence",
            "similarity_score": 0.5692417025566101,
        },
        {
            "name": "math-function-off",
            "glyph": "f15e",
            "keywords": "math-function-off, statyscics, linear, math, off, function, graph",
            "similarity_score": 0.5677418112754822,
        },
        {
            "name": "variable-off",
            "glyph": "f1bd",
            "keywords": "variable, science, calculate, variable-off, maths, mathematics, off, function",
            "similarity_score": 0.5666729807853699,
        },
        {
            "name": "sort-descending-2",
            "glyph": "eee3",
            "keywords": "sort, descending, sort-descending-2, filter, order, arrange, 2, classify",
            "similarity_score": 0.5658097863197327,
        },
        {
            "name": "chart-pie-off",
            "glyph": "f3d3",
            "keywords": "data, chart, diagram, pie, analysis, rhythm, graph, off, chart-pie-off, statistics",
            "similarity_score": 0.5640719532966614,
        },
        {
            "name": "test-pipe-off",
            "glyph": "f1b1",
            "keywords": "sample, test, off, test-pipe-off, pipe, color",
            "similarity_score": 0.5618718862533569,
        },
        {
            "name": "chart-pie-2",
            "glyph": "ee31",
            "keywords": "data, chart, diagram, pie, analysis, 2, rhythm, graph, chart-pie-2, statistics",
            "similarity_score": 0.5598427653312683,
        },
        {
            "name": "triangle-off",
            "glyph": "ef02",
            "keywords": "triangle, off, triangle-off, delta",
            "similarity_score": 0.5595081448554993,
        },
        {
            "name": "a-b-2",
            "glyph": "f25f",
            "keywords": "visual, a-b-2, user, test, a, b, 2",
            "similarity_score": 0.559417724609375,
        },
        {
            "name": "ease-in-out",
            "glyph": "f572",
            "keywords": "ease-in-out, in, ease, curve, graph, function, out, animation",
            "similarity_score": 0.5573281049728394,
        },
        {
            "name": "test-pipe-2",
            "glyph": "f0a4",
            "keywords": "sample, test, test-pipe-2, pipe, 2, color",
            "similarity_score": 0.5566393136978149,
        },
        {
            "name": "a-b-off",
            "glyph": "f0a6",
            "keywords": "a-b-off, visual, user, test, off, a, b",
            "similarity_score": 0.5560680031776428,
        },
        {
            "name": "cone-off",
            "glyph": "f3d8",
            "keywords": "shape, cone-off, cone, geometry, object, math, off",
            "similarity_score": 0.5556488037109375,
        },
        {
            "name": "analyze-filled",
            "glyph": "f719",
            "keywords": "data, analyze, analyze-filled, analytics, graph, filled, statistics",
            "similarity_score": 0.5555199980735779,
        },
        {
            "name": "math-x-minus-y",
            "glyph": "f4f3",
            "keywords": "x, expression, y, minus, equation, mathematic, math, math-x-minus-y",
            "similarity_score": 0.5554648041725159,
        },
        {
            "name": "chart-donut-2",
            "glyph": "ee2c",
            "keywords": "data, chart, diagram, analysis, donut, 2, rhythm, graph, chart-donut-2, statistics",
            "similarity_score": 0.5553399324417114,
        },
        {
            "name": "text-recognition",
            "glyph": "f204",
            "keywords": "recognition, text, processing, text-recognition, detection, language",
            "similarity_score": 0.5552355051040649,
        },
        {
            "name": "ease-in",
            "glyph": "f573",
            "keywords": "in, ease, curve, graph, function, ease-in, animation",
            "similarity_score": 0.5547121167182922,
        },
        {
            "name": "chart-bar-off",
            "glyph": "f3d2",
            "keywords": "data, chart, diagram, analysis, bar, chart-bar-off, rhythm, graph, off, statistics",
            "similarity_score": 0.5543516278266907,
        },
        {
            "name": "sort-descending",
            "glyph": "eb27",
            "keywords": "sort, descending, filter, order, sort-descending, arrange, classify",
            "similarity_score": 0.5543385148048401,
        },
        {
            "name": "chart-radar",
            "glyph": "ed77",
            "keywords": "variable, two, dimensions, points, data, chart, value, radar, report, chart-radar, statistics",
            "similarity_score": 0.5524773001670837,
        },
        {
            "name": "chart-arrows-vertical",
            "glyph": "ee29",
            "keywords": "variable, arrows, decrease, data, chart-arrows-vertical, chart, level, statistical, vertical, value, increase, scale, statistics",
            "similarity_score": 0.5524771809577942,
        },
        {
            "name": "ease-out",
            "glyph": "f575",
            "keywords": "ease, ease-out, curve, graph, function, out, animation",
            "similarity_score": 0.5522830486297607,
        },
        {
            "name": "chart-dots-2",
            "glyph": "f097",
            "keywords": "variable, data, chart, diagram, statistical, graph, dots, value, analyticks, chart-dots-2, scale, statistics, 2",
            "similarity_score": 0.5509803891181946,
        },
        {
            "name": "math-x-divide-y",
            "glyph": "f4f1",
            "keywords": "x, expression, y, equation, mathematic, math, divide, math-x-divide-y",
            "similarity_score": 0.5508686900138855,
        },
        {
            "name": "test-pipe",
            "glyph": "eb3a",
            "keywords": "test-pipe, sample, test, pipe, color",
            "similarity_score": 0.5506420731544495,
        },
    ]
}


query_prompt: str = "Represent this sentence for searching relevant passages:"
search_string: str = "inference"

rerank_input_query = f"{query_prompt} {search_string}"
rerank_input_documents = [result["keywords"] for result in icon_results["result"]]

rerank_results = rerank_model.rank(
    rerank_input_query,
    rerank_input_documents,
    return_documents=True,
)

icon_list = []
for item in rerank_results:
    icon = {}
    # add "score": item['score'] as a new key to the list item in icon_results["results"] with index equal to item['corpus_id']
    icon["name"] = icon_results["result"][item["corpus_id"]]["name"]
    icon["glyph"] = icon_results["result"][item["corpus_id"]]["glyph"]
    icon["score"] = item["score"]
    icon_list.append(icon)

ic(rerank_results)
ic(icon_list)
