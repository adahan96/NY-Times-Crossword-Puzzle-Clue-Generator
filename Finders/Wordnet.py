import nltk
from nltk.corpus import wordnet as wn

class Wordnet():
    def __init__(self):
        nltk.download('wordnet')

    @staticmethod
    def findFromWordnet(word, synonyms, antonyms, definitions, examples):

        # Synonym set of the word
        synset = wn.synsets(word)
        for syn in synset:
            for l in syn.lemmas():
                synonyms.append(l.name())
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())
            definitions.append(syn.definition())
            examples += syn.examples()
