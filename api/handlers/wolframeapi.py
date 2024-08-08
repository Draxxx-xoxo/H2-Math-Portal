import requests
import os

app_id = os.environ.get("WOLFRAM_APP_ID")
url = os.environ.get("WOLFRAM_URL")

def wolfram_api(query):

    params = {
        "i": query,
        "appid": app_id,
    }
    
    response = requests.get(url, params=params)

    print(response.url)
    
    if response.status_code == 200:
        return response.text
    else:
        return "Could not connect to Wolfram Alpha API" + f"[{response.status_code}]"



