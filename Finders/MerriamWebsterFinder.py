import requests


def findFromMWDictionary(word):
    """Search word in Merriam-Webster Dictionary
    https://dictionaryapi.com/products/api-collegiate-dictionary

    Arguments:
        word {string} -- [description]

    Returns:
        [string, string] -- [Short definition and example sentence]
    """
    response = requests.get(
        f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}",
        params={
            "key": "9b7981b7-6045-4b18-9a42-a123b14679d6"
        }
    )

    jsonResponse = response.json()
    if len(jsonResponse) != 0:
        try:
            definition = jsonResponse[0]["shortdef"][0]
        except Exception:
            definition = None

        try:
            exampleSentence = jsonResponse[0]["suppl"]["examples"][0]["t"]
        except Exception:
            exampleSentence = None
        return definition, exampleSentence
    else:
        return None, None


def findFromMWThesaurus(word):
    """Search word in Merriam-Webster Thesaurus
    https://dictionaryapi.com/products/api-collegiate-thesaurus

    Arguments:
        word {string} -- [description]

    Returns:
        [string, string] -- [Synonym and antonym]
    """
    response = requests.get(
        f"https://dictionaryapi.com/api/v3/references/thesaurus/json/{word}",
        params={
            "key": "39852832-1829-4acf-9795-46a52dc14d75"
        }
    )

    jsonResponse = response.json()
    if len(jsonResponse) != 0:
        try:
            synonym = jsonResponse[0]["meta"]["syns"][0][0]
        except Exception:
            synonym = None
        try:
            antonym = jsonResponse[0]["meta"]["ants"][0][0]
        except Exception:
            antonym = None

        return synonym, antonym
    else:
        return None, None
