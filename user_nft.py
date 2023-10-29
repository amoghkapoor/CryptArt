import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_key = os.getenv("minter_key")

def user_nft(address, chain):
    query_params = {
        "chain": chain,
        "page_size": 50,
        "continuation": None,
        "include": "file_information"
    }

    headers = {
        "accept": "application/json",
        "Authorization": API_key
    }

    url = "https://api.nftport.xyz/v0/accounts/{}".format(address)

    response = requests.get(
        url,
        headers=headers,
        params=query_params,
    )

    return(json.loads(response.text))
