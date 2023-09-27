import json

import elasticsearch as es

from flask import Flask

app = Flask(__name__)
client = es.Elasticsearch([{'host': 'localhost', 'port': 9500, 'scheme': 'https'}],
                          basic_auth=("elastic", "*iiFGM_ss*YOGU0x1pOC"),
                          verify_certs=False,
                          ssl_show_warn=False)
data = json.load(open("out.json", "r"))


@app.route("/")
def hello():
    return """<script src=static/script.js></script>
    <input type='text' id='search_bar' placeholder='Search' oninput='doSearch()'>
    <div id='search_results'></div>
    """


@app.route("/search/<query>", methods=["GET"])
def search(query):
    result = client.search(index="jvet_documents", query={"match": {"text": query}}, size=50)
    out = {}
    for x in result.body["hits"]["hits"]:
        try:
            split_id = x["_id"].split(".")[0]
            out[split_id] = data[split_id]
        except KeyError:
            pass
    return out
