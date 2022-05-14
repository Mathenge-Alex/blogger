from webbrowser import get
import requests
from pprint import pprint
import json
from urllib.request import urlopen

API = "http://quotes.stormconsultancy.co.uk/random.json"

def get_quotes():
    with urlopen(API) as resp:
        # breakpoint()
        # json.dumps +> to a javascript obj
        #
        data = json.loads(resp.read())

        print(data)


class Quote(object):
    def __init__(self, quote, author, permalink, id):
        # def __init__(self, quote, author, permalink, **kwargs): This allows one to leave alone all other unnecessary data. 
        self.quote = quote
        self.permalink = permalink
        self.author = author
        self.id = id
        
    def __str__(self) -> str:
        return self.author

def get_random_quote():
    'Method calling random API endpoint and returns a random quote'
    response = requests.get(API)
    data = response.json()
    print (Quote(**data))   # Kwargs

    #  Same as quote = Quote(quote = data.get('quote'))


if __name__ =='__main__':
    get_random_quote()
    