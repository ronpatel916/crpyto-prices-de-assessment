import os
from dotenv import load_dotenv
import requests
from tenacity import retry, stop_after_attempt, wait_fixed


load_dotenv()

API_KEY = os.getenv("COINMARKETCAP_API_KEY")
API_BASE_URL = 'https://pro-api.coinmarketcap.com/'

def get_headers():
    return {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY
    }

@retry(stop=stop_after_attempt(3), wait = wait_fixed(20))
def fetch_data(endpoint, parameters = None):
    url = API_BASE_URL + endpoint
    headers = get_headers()
    try:
        response = requests.get(url, headers=headers,params=parameters)
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        raise