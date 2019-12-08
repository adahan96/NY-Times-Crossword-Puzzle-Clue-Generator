from bs4 import BeautifulSoup
import requests

def didyoumean(word):
    link = "https://www.google.com/search?q=" + word
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    source = requests.get(link, headers=headers).text
    soup = BeautifulSoup(source, "html.parser")
    res = soup.find('div', class_="med")

    if res.text == '  ':
        return word
    else:

        return res.text.replace('Bunu mu demek istediniz? ','')
