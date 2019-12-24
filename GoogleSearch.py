from bs4 import BeautifulSoup
import requests


def getDidyoumeanSuggestion(word):
    """Search the word in Google and return the "Did you mean" suggestion result

    Arguments:
        word {string} -- [word that will be searched]

    Returns:
        [string] -- [Return suggestion result if exists, else return None]
    """
    link = "https://www.google.com/search?q=" + word
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    source = requests.get(link, headers=headers).text
    soup = BeautifulSoup(source, "html.parser")
    res = soup.find('div', class_="med")

    if '#foot{visibility:inherit}Bunu mu demek istediniz? ' in soup.text:
        correctedWord = res.text.replace('Bunu mu demek istediniz? ', '')
        print("[GOOGLE'S DID YOU MEAN] Corrected the word as", correctedWord)
        return correctedWord
    else:
        return None
