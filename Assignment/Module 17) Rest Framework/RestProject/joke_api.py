import requests

def fetch_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    try:
        response = requests.get(url)
        response.raise_for_status()
        joke = response.json()
        print(f"--- Random Joke ---")
        print(f"Setup: {joke['setup']}")
        print(f"Punchline: {joke['punchline']}")
    except Exception as e:
        print(f"Error fetching joke: {e}")

if __name__ == "__main__":
    fetch_joke()
