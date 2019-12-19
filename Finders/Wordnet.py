import nltk
from nltk.corpus import wordnet as wn

class Wordnet:
    @staticmethod
    def findFromWordnet(word, synonyms, antonyms, definitions, examples):
        nltk.download("wordnet")
        # Synonym set of the word
        for w in word:
            synset = wn.synsets(w)
            for i in range(len(synset)):
                if i == 0:

                    lemma = synset[0].lemmas()[0]
                    # for l in synset[0].lemmas():

                    print('')
                    # synonym = l.name().replace('_', " ")
                    # print("[WORDNET] Found a synonym for", word, ":", synonym)
                    # synonyms.add(synonym)
                    if lemma.antonyms():
                        for a in lemma.antonyms():

                            antonym = a.name()
                            print("[WORDNET] Found an antonym for", word, ":", antonym)
                            antonyms.add(antonym)
                    if i < 3:

                        definition = synset[i].definition()
                        print("[WORDNET] Found a definition for", word, ":", definition)
                        definitions.add(definition)

                        exs = synset[i].examples()
                        print("[WORDNET] Found example sentences for", word, ":", exs)
                        for e in exs:
                            examples.add(e)
        #print('')

#Wordnet.findFromWordnet('',set(),set(),[],[])