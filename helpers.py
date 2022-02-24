import os
import requests
import urllib.parse

from flask import request

def lookup(query):

    # Contact Google API

    try:
        #api_key = os.environ.get("API_KEY")
        url = f"https://www.googleapis.com/books/v1/volumes?q={urllib.parse.quote_plus(query)}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parsing response
    try:
        result = response.json()
        return
    except (KeyError, TypeError, ValueError):
        return None


