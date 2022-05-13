from poplib import POP3_PORT
import requests
from pprint import pprint

API = "http://quotes.stormconsultancy.co.uk/random.json"

def get_random_quote():
    'Method calling random API endpoint and returns a random quote'
    response = requests.get(API)
    data = response.json()
    pprint(data)

if __name__ =='__main__':
    get_random_quote()
    