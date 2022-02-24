import os
import requests
import urllib.parse

def lookup(query):

    # Contact Google Books API
    try:
        #api_key = os.environ.get("API_KEY")
        url = f"https://www.googleapis.com/books/v1/volumes?q={urllib.parse.quote_plus(query)}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # parsing response
    try:
        results = response.json()
        return
    except (KeyError, TypeError, ValueError):
        return None
