import requests

def fetch_random_joke():
    """
    Module 17, Lab 1 & Practical 1:
    Write a Python script to fetch a random joke from an API and display it on the console.
    """
    url = "https://official-joke-api.appspot.com/random_joke"
    
    try:
        response = requests.get(url)
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse the JSON response
        joke_data = response.json()
        
        # Display the joke
        print("Here is a random joke for you:")
        print(f"Setup: {joke_data.get('setup')}")
        print(f"Punchline: {joke_data.get('punchline')}")
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the joke: {e}")

if __name__ == "__main__":
    fetch_random_joke()
