<<<<<<< HEAD
import requests
import urllib.parse

from flask import request

def lookup(query):

    # Contact Google API
=======
import os
import requests
import urllib.parse

def lookup(query):

    # Contact Google Books API
>>>>>>> bb103f561bbd69012c90f82cab7f241e6eea5a4b
    try:
        #api_key = os.environ.get("API_KEY")
        url = f"https://www.googleapis.com/books/v1/volumes?q={urllib.parse.quote_plus(query)}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

<<<<<<< HEAD
    # Parsing response
    try:
        result = response.json()
        return
    except (KeyError, TypeError, ValueError):
        return None


=======
    # parsing response
    try:
        results = response.json()
        return
    except (KeyError, TypeError, ValueError):
        return None
>>>>>>> bb103f561bbd69012c90f82cab7f241e6eea5a4b
