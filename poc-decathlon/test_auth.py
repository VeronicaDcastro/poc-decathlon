import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("JIRA_BASE_URL") + "/rest/api/3/myself"
username = os.getenv("JIRA_EMAIL")
api_token = os.getenv("JIRA_API_TOKEN")

response = requests.get(url, auth=(username, api_token))

print("Status code:", response.status_code)
try:
    print("Response JSON:", response.json())
except Exception as e:
    print("Erro ao tentar mostrar JSON:", e)
