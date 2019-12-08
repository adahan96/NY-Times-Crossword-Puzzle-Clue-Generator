import random
from concurrent.futures import ThreadPoolExecutor
from Finders.AntonymFinder import findAntonym
from Finders.DictionaryFinder import findDefinitionFromDictionary
from Finders.ExampleSentenceFinder import findExampleSentence
from Finders.HomonymFinder import findHomonym
from Finders.SpinnerFinder import findSpinner
from Finders.DatamuseFinder import findFromDatamuse
from Finders.Wordnet import Wordnet as WT


class Clue:
    def __init__(self, realClue, answer):
        self.realClue = realClue
        self.answer = answer
        self.newClues = []
        self.definitions = []
        self.synonyms = []
        self.example_sentences = []
        self.spinner = []

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
            self.findHomonym,
            self.findSpinner,
            self.searchDatamuse
        ])

    def filterNewClues(self):
        """New clues that are similar to real clue should be removed from
        newClues list
        """
        print("Filtering new clues not yet implemented")

    def getRandomNewClue(self):
        if len(self.newClues) == 0:
            return None
        else:
            return random.choice(self.newClues)

    def lookUpDictionaries(self):
        result = findDefinitionFromDictionary(self.answer)
        if result is not None:
            self.newClues.append(result)

    def findFromWordnet(self):
        wordnet = WT()
        wordnet.findClues(self.answer)

        """
        if result is not None:
            self.newClues.append(result)
        """
    def findAntonym(self):
        result = findAntonym(self.answer)
        if result is not None:
            self.newClues.append(result)

    def findExampleSentence(self):
        result = findExampleSentence(self.answer)
        if result is not None:
            self.newClues.append(result)

    def findHomonym(self):
        result = findHomonym(self.answer)
        if result is not None:
            self.newClues.append(result)

    def findSpinner(self):
        result = findSpinner(self.realClue)
        if result is not None:
            self.newClues.append(result)

    def searchDatamuse(self):
        result = findFromDatamuse(self.answer)
        if result is not None:
            self.newClues.append(result)
