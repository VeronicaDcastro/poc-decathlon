from dotenv import load_dotenv
import os
import requests

# Carrega as variáveis do .env
load_dotenv()

# --- JIRA ---
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

# --- CONFLUENCE ---
CONFLUENCE_BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
CONFLUENCE_EMAIL = os.getenv("CONFLUENCE_EMAIL")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")

def search_jira(query, max_results=5):
    jql = f'summary ~ "{query}" OR description ~ "{query}"'
    url = f"{JIRA_BASE_URL}/rest/api/3/search"

    response = requests.get(
        url,
        headers={"Accept": "application/json"},
        auth=(JIRA_EMAIL, JIRA_API_TOKEN),
        params={"jql": jql, "maxResults": max_results}
    )

    if response.status_code != 200:
        print(f"[JIRA] Erro {response.status_code}: {response.text}")
        return []

    issues = response.json().get("issues", [])
    return [
        {
            "source": "jira",
            "key": issue["key"],
            "summary": issue["fields"]["summary"],
            "url": f"{JIRA_BASE_URL}/browse/{issue['key']}"
        }
        for issue in issues
    ]

def search_confluence(query, max_results=5):
    cql = f'text ~ "{query}" AND type = page'
    url = f"{CONFLUENCE_BASE_URL}/rest/api/content/search"

    response = requests.get(
        url,
        headers={"Accept": "application/json"},
        auth=(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN),
        params={"cql": cql, "limit": max_results}
    )

    if response.status_code != 200:
        print(f"[Confluence] Erro {response.status_code}: {response.text}")
        return []

    pages = response.json().get("results", [])
    return [
        {
            "source": "confluence",
            "id": page["id"],
            "title": page["title"],
            "url": f"{CONFLUENCE_BASE_URL}/pages/{page['id']}"
        }
        for page in pages
    ]

def run_search(query):
    print(f"\n🔍 Buscando por: {query}\n")

    jira_results = search_jira(query)
    confluence_results = search_confluence(query)

    all_results = jira_results + confluence_results

    if not all_results:
        print("Nenhum resultado encontrado.")
        return

    for result in all_results:
        if result["source"] == "jira":
            print(f"[JIRA] {result['key']} - {result['summary']} ({result['url']})")
        elif result["source"] == "confluence":
            print(f"[CONFLUENCE] {result['title']} ({result['url']})")

# 🔽 Executa ao rodar no terminal
if __name__ == "__main__":
    run_search("Documento administrativo")

def test_confluence(query):
    cql = f'text ~ "{query}" AND type = page'
    url = f"{CONFLUENCE_BASE_URL}/rest/api/content/search"

    response = requests.get(
        url,
        headers={"Accept": "application/json"},
        auth=(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN),
        params={"cql": cql, "limit": 5}
    )

    print("Status Code:", response.status_code)
    print("Resposta bruta:", response.text)

if __name__ == "__main__":
    test_confluence("Documento Administrativo")
