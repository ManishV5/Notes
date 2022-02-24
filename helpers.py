import requests
import urllib.parse

def lookup(query):

    # Contact Google API
    try:
        #api_key = os.environ.get("API_KEY")
        url = "https://www.googleapis.com/books/v1/volumes?q={urllib.parse.quote_plus(query)}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parsing response
    try:
        result = response.json()
        print(result)
        return {
            "total": result["totalItems"]
        }

    except (KeyError, TypeError, ValueError):
        return None
