import nltk
from nltk.corpus import wordnet as wn


def findFromWordnet(word):
    antonym, definition, exampleSentence = None, None, None
    nltk.download("wordnet", quiet=True)
    # Synonym set of the word
    synsets = wn.synsets(word)
    if len(synsets) != 0:
        synset = synsets[0]
        lemma = synset.lemmas()[0]

        # Add only the first antonym, definition and example sentence
        if lemma.antonyms():
            antonym = lemma.antonyms()[0].name()
        if synset.definition():
            definition = synset.definition()
            # TODO: Definition of email, key and app couldn't find in Wordnet on 24/12/2019. Code may be broken, should be fixed
        if synset.examples():
            exampleSentence = synset.examples()[0]

    return antonym, definition, exampleSentence
