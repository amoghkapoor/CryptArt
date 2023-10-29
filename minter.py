import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_key = os.getenv("minter_key")

def mint_on_polygon(file_url, extension, name, description, address):
    query_params = {
        "chain": "polygon",
        "name": name,
        "description": description,
        "mint_to_address": address
    }

    file = open(name+'.'+extension, 'wb')
    file.write(requests.get(file_url).content)
    file.close()
    file = open(name + '.' + extension, 'rb')

    response = requests.post(
        "https://api.nftport.xyz/v0/mints/easy/files",
        headers={"Authorization": API_key},
        params=query_params,
        files={"file": file}
    )

    file.close()
    os.remove(name+'.'+extension)


    #print(response.text)
    return response.text


def mint_on_eth(file_url, extension, name, description, address):
    query_params = {
        "chain": "goerli",
        "name": name,
        "description": description,
        "mint_to_address": address
    }

    file = open(name+'.'+extension, 'wb')
    file.write(requests.get(file_url).content)
    file.close()
    file = open(name + '.' + extension, 'rb')

    response = requests.post(
        "https://api.nftport.xyz/v0/mints/easy/files",
        headers={"Authorization": API_key},
        params=query_params,
        files={"file": file}
    )

    file.close()
    os.remove(name+'.'+extension)


    #print(response.text)
    return response.text


