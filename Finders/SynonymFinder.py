import nltk
from nltk.corpus import wordnet as wn


def findSynonym(word):
    # Synonym set of the word)
    nltk.download('wordnet')
    synset = wn.synsets(str('bat'))
    synonyms, antonyms, definitions, examples = [], [], [], []
    for syn in synset:
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
        definitions.append(syn.definition())
        examples += syn.examples()

    print('')
    #print("Find synonyms not yet implemented")