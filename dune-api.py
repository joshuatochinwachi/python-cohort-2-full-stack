import os
import requests

dune_api_key = os.getenv("DEFI_JOSH_DUNE_QUERY_API_KEY")

if not dune_api_key:
    raise ValueError("API key not found in environment variables")

query_ids = []  

headers = {"X-DUNE-API-KEY": dune_api_key}

for query_id in query_ids:
    url = f"https://api.dune.com/api/v1/query/{query_id}/execute"
    response = requests.post(url, headers=headers)
    print(f"Query {query_id}: {response.status_code} - {response.text}")