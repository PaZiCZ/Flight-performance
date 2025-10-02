# joke.py
import requests
from bs4 import BeautifulSoup

def get_joke_of_the_day():
    url = "https://jokesoftheday.net/"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "Failed to retrieve the joke."

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the first joke block with class 'jokeContent'
    joke_block = soup.find("div", class_="jokeContent")
    if not joke_block:
        return "Joke of the day not found."

    # Extract only the question + answer (ignore title)
    p_tag = joke_block.find("p")
    if p_tag:
        return p_tag.get_text(strip=True, separator="\n")

    return joke_block.get_text(strip=True, separator="\n")