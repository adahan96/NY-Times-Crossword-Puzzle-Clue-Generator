import requests
from bs4 import BeautifulSoup


def findFromUrbanDictionary(word):
    r = requests.get(
        "http://www.urbandictionary.com/define.php?term={}".format(word))
    soup = BeautifulSoup(r.content, features="html.parser")

    try:
        meaning = soup.find("div", attrs={"class": "meaning"}).text
    except Exception:
        meaning = None

    try:
        exampleSentence = soup.find("div", attrs={"class": "example"}).text
    except:
        exampleSentence = None

    return meaning, exampleSentence
