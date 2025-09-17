from flask import Flask, request, jsonify
from search_all import search_jira, search_confluence

app = Flask(__name__)

@app.route("/search", methods=["POST"])
def search():
    data = request.json
    query = data.get("query")

    if not query:
        return jsonify({"error": "Você precisa enviar o campo 'query'."}), 400

    jira_results = search_jira(query)
    confluence_results = search_confluence(query)

    all_results = jira_results + confluence_results

    return jsonify({"results": all_results})

if __name__ == "__main__":
    app.run(debug=True)
