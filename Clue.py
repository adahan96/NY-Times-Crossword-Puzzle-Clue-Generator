import random
import spacy
from concurrent.futures import ThreadPoolExecutor
from Finders.AntonymFinder import findAntonym
from Finders.DictionaryFinder import findDefinitionFromDictionary
from Finders.ExampleSentenceFinder import findExampleSentence
from Finders.HomonymFinder import findHomonym
from Finders.SpinnerFinder import findSpinner
from Finders.DatamuseFinder import findFromDatamuse
from Finders.MerriamWebsterFinder import findFromMWDictionary, findFromMWThesaurus
from Finders.Wordnet import Wordnet
from GoogleSearch import didyoumean

class Clue:
    def __init__(self, realClue, answer):
        self.realClue = realClue
        self.answer = didyoumean(answer)
        self.newClues = set()
        self.definitions = set()
        self.synonyms = set()
        self.antonyms = set()
        self.example_sentences = []
        self.spinner = []

        # Initialization
        self.nlp = spacy.load('en_core_web_sm')

    def generateNewClues(self):
        def run_io_tasks_in_parallel(tasks):
            with ThreadPoolExecutor() as executor:
                running_tasks = [executor.submit(task) for task in tasks]
                for running_task in running_tasks:
                    running_task.result()

        run_io_tasks_in_parallel([
            self.lookUpDictionaries,
            self.findFromWordnet,
            self.findAntonym,
            self.findExampleSentence,
            self.findSpinner,
            self.searchDatamuse,
            self.findFromMWDictionary,
            self.findFromMWThesaurus
        ])
        self.preprocess_clues()

    def filterNewClues(self):
        """New clues that are similar to real clue should be removed from
        newClues list
        """
        threshold = 0.45

        realClue_nlp = self.nlp(self.realClue)
        filteredClues = []
        for clue in self.newClues:
            clue_nlp = self.nlp(clue)
            similarity_percent = realClue_nlp.similarity(clue_nlp)
            if similarity_percent < threshold:
                filteredClues.append(clue)

        self.newClues = filteredClues

        # make everything lower in new clues but first letter
        self.newClues = [clue.lower() for clue in self.newClues]
        self.newClues = [clue.capitalize() for clue in self.newClues]
        self.newClues = set(self.newClues)

    def getRandomNewClue(self):
        if len(self.newClues) == 0:

            print('')
            return None
        else:
            return random.choice(list(self.newClues))

    def lookUpDictionaries(self):
        result = findDefinitionFromDictionary(self.answer)
        if result is not None:
            self.definitions.append(result)

    def findFromWordnet(self):
        Wordnet.findFromWordnet(self.answer, self.synonyms, self.antonyms, self.definitions, self.example_sentences)

    def findAntonym(self):
        result = findAntonym(self.answer)
        if result is not None:
            self.antonyms.add(result)

    def findExampleSentence(self):
        result = findExampleSentence(self.answer)
        if result is not None:
            self.example_sentences.append(result)

    def findSpinner(self):
        result = findSpinner(self.realClue)
        if result is not None:
            self.newClues.add(result)

    def searchDatamuse(self):
        result = findFromDatamuse(self.answer)
        if result is not None:
            self.newClues.add(result)
    
    def findFromMWDictionary(self):
        definition, sentence = findFromMWDictionary(self.answer)
        if definition is not None:
            self.definitions.add(definition)
        if sentence is not None:
            self.example_sentences.append(sentence)
    
    def findFromMWThesaurus(self):
        synonym, antonym = findFromMWThesaurus(self.answer)
        if synonym is not None:
            self.synonyms.add(synonym)
        if antonym is not None:
            self.antonyms.add(antonym)

    def preprocess_clues(self):
        self.preprocess_example_sentences()
        self.preprocess_antonyms()
        self.preprocess_synonyms()
        self.preprocess_definitions()

    def preprocess_example_sentences(self):
        for exs in self.example_sentences:
            if self.answer.lower() in exs:
                self.newClues.add(exs.replace(self.answer.lower(), '___'))
            else:
                pass
                #print('Answer not in example sentence')

    def preprocess_definitions(self):
        for definition in self.definitions:
            if len(definition.split(' ')) < 9 and self.answer.lower() not in definition.lower():
                self.newClues.add(definition)
        print('')

    def preprocess_antonyms(self):
        for antonym in self.antonyms:
            new_antonym = 'Opposite of ' + antonym
            self.newClues.add(new_antonym)

    def preprocess_synonyms(self):
        for synonym in self.synonyms:
            l = synonym.lower()
            if l.find(self.answer.lower()) == -1:
                self.newClues.add(l)
            else:
                pass