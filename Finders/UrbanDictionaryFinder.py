import requests
from bs4 import BeautifulSoup


def findFromUrbanDictionary(word):
    r = requests.get(
        "http://www.urbandictionary.com/define.php?term={}".format(word))
    soup = BeautifulSoup(r.content, features="html.parser")

    try:
        allMeanings = [element.text for element in soup.find_all(
            "div", attrs={"class": "meaning"})]
        meaning = min(allMeanings, key=len)  # Get the shortest meaning
    except Exception:
        meaning = None

    try:
        allExampleSentences = [element.text for element in soup.find_all(
            "div", attrs={"class": "example"})]
        # Get the shortest example sentence
        exampleSentence = min(allExampleSentences, key=len)
    except:
        exampleSentence = None

    return meaning, exampleSentence
