import nltk
from nltk.corpus import wordnet as wn

class Wordnet:
    @staticmethod
    def findFromWordnet(word, synonyms, antonyms, definitions, examples):
        nltk.download("wordnet")
        # Synonym set of the word
        synset = wn.synsets(word)
        for syn in synset:
            for l in syn.lemmas():

                synonyms.add(l.name().replace('_', " "))
                if l.antonyms():
                    for a in l.antonyms():
                        antonyms.add(a.name())
            definitions.append(syn.definition())
            examples += syn.examples()
        #print('')

#Wordnet.findFromWordnet('',set(),set(),[],[])