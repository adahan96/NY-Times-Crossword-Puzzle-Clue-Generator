import requests


def findFromDatamuse(word):
    response = requests.get(
        "https://api.datamuse.com/words",
        params={
            "ml": word
        }
    )

    jsonResponse = response.json()
    if len(jsonResponse) != 0:
        return jsonResponse[0]["word"]
    else:
        return None
