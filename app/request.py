import requests
from .models import Quote

# Random Quote API
api = "http://quotes.stormconsultancy.co.uk/random.json"


def get_random_quote():
    random_quote = requests.get(api).json()

    quote = Quote(random_quote.get('author'), random_quote.get('quote'))

    return quote
    pass