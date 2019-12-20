import requests


def findFromDatamuse(word):
    THRESHOLD = 20000

    response = requests.get(
        "https://api.datamuse.com/words",
        params={
            "ml": word
        }
    )

    jsonResponse = response.json()
    if len(jsonResponse) != 0 and jsonResponse[0]["score"] >= THRESHOLD:
        return jsonResponse[0]["word"]
    else:
        return None
