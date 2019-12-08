import nltk
from nltk.corpus import wordnet as wn


class Wordnet:
    def __init__(self, synonym = [],antonym = [],definition = [],example = []):
        self.synonym = synonym
        self.antonym = antonym
        self.definition = definition
        self.example = example


    def findClues(self,word):
        # Synonym set of the word)
        nltk.download('wordnet')
        synset = wn.synsets(str('bat'))
        for syn in synset:
            for l in syn.lemmas():
                self.synonym.append(l.name())
                if l.antonyms():
                    self.antonym.append(l.antonyms()[0].name())
            self.definition.append(syn.definition())
            self.example += syn.examples()
        #print("Find synonyms not yet implemented")