from dotenv import load_dotenv
import os
import requests

# Carrega variáveis do .env
load_dotenv()

def run(params):
    base_url = os.getenv("JIRA_BASE_URL")
    username = os.getenv("JIRA_EMAIL")
    api_token = os.getenv("JIRA_API_TOKEN")

    # Teste para ver se as variáveis estão sendo carregadas
    print("URL:", base_url)
    print("Email:", username)
    print("API Token:", api_token[:5] + "...")

    query = params["query"]
    
    # resto do código continua...
    query = params["query"]

    jql = f'summary ~ "{query}" OR description ~ "{query}"'
    url = f"{base_url}/rest/api/3/search"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.get(
        url,
        headers=headers,
        auth=(username, api_token),
        params={"jql": jql, "maxResults": 5}
    )

    response.raise_for_status()
    issues = response.json()["issues"]

    return {
        "results": [
            {
                "key": issue["key"],
                "summary": issue["fields"]["summary"],
                "url": f"{base_url}/browse/{issue['key']}"
            }
            for issue in issues
        ]
    }

# 🔍 Teste local
if __name__ == "__main__":
    resultado = run({"query": "bolo de laranja"})
    for item in resultado["results"]:
        print(f"{item['key']} - {item['summary']} ({item['url']})")
