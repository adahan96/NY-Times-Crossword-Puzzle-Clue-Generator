import random
import spacy
from concurrent.futures import ThreadPoolExecutor
from Finders.AntonymFinder import findAntonym
from Finders.DictionaryFinder import findDefinitionFromDictionary
from Finders.ExampleSentenceFinder import findExampleSentence
from Finders.SpinnerFinder import findSpinner
from Finders.DatamuseFinder import findFromDatamuse
from Finders.MerriamWebsterFinder import findFromMWDictionary, findFromMWThesaurus
from Finders.Wordnet import Wordnet
from Finders.UrbanDictionaryFinder import findFromUrbanDictionary
from GoogleSearch import didyoumean


class Clue:
    def __init__(self, realClue, answer):

        answer = answer.lower()

        self.realClue = realClue
        self.answer = set()
        self.answer.add(answer)

        corrected_answer, is_word_corrected = didyoumean(answer)
        if is_word_corrected:
            self.answer.add(corrected_answer)

        self.definitions = set()
        self.newClues = set()
        self.definitions = set()
        self.synonyms = set()
        self.antonyms = set()
        self.example_sentences = set()
        self.spinner = set()

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
            self.findFromMWThesaurus,
            self.findUrbanDictionary
        ])
        self.preprocess_clues()

    def filterNewClues(self):
        """New clues that are similar to real clue should be removed from
        newClues list
        """
        threshold = 0.80

        realClue_nlp = self.nlp(self.realClue)
        filteredClues = set()
        for clue in self.newClues:
            clue_nlp = self.nlp(clue)
            similarity_percent = realClue_nlp.similarity(clue_nlp)
            if similarity_percent < threshold:
                filteredClues.add(clue)

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
            self.definitions.add(result)

    def findFromWordnet(self):
        Wordnet.findFromWordnet(
            self.answer, self.synonyms, self.antonyms, self.definitions, self.example_sentences)

    def findAntonym(self):
        result = findAntonym(self.answer)
        if result is not None:
            self.antonyms.add(result)

    def findExampleSentence(self):
        result = findExampleSentence(self.answer)
        if result is not None:
            self.example_sentences.add(result)

    def findSpinner(self):
        result = findSpinner(self.realClue)
        if result is not None:
            self.newClues.add(result)

    def searchDatamuse(self):
        for answer in self.answer:
            result = findFromDatamuse(answer)
            if result is not None:
                print("[DATAMUSE] Found a clue for", answer, ":", result)
                self.newClues.add(result)

    def findFromMWDictionary(self):
        for answer in self.answer:
            definition, sentence = findFromMWDictionary(answer)
            if definition is not None:
                print("[MERRIAM WEBSTER] Found a definition for", answer, ":", definition)
                self.definitions.add(definition)
            if sentence is not None:
                print("[MERRIAM WEBSTER] Found an example sentence for", answer, ":", sentence)
                self.example_sentences.append(sentence)

    def findFromMWThesaurus(self):
        for answer in self.answer:
            synonym, antonym = findFromMWThesaurus(answer)
            if synonym is not None:
                print("[MERRIAM WEBSTER] Found a synonym for", answer, ":", synonym)
                self.synonyms.add(synonym)
            if antonym is not None:
                print("[MERRIAM WEBSTER] Found an antonym for", answer, ":", antonym)
                self.antonyms.add(antonym)

    def findUrbanDictionary(self):
        for answer in self.answer:
            meaning, example = findFromUrbanDictionary(answer)
            if meaning is not None:
                self.definitions.add(meaning)
            if example is not None:
                self.example_sentences.add(example)

    def preprocess_clues(self):
        self.preprocess_example_sentences()
        self.preprocess_antonyms()
        self.preprocess_synonyms()
        self.preprocess_definitions()
        self.newClueprocess()

    def preprocess_example_sentences(self):
        max_word_number = 13
        for answer in self.answer:
            for exs in self.example_sentences:
                if answer.lower() in exs and len(exs.split(' ')) < max_word_number:
                    self.newClues.add(exs.replace(answer.lower(), '___'))
                else:
                    pass
                    #print('Answer not in example sentence')

    def preprocess_definitions(self):
        ayberk_magic = 13
        for definition in self.definitions:
            for answer in self.answer:
                if len(definition.split(' ')) < ayberk_magic and answer.lower() not in definition.lower():
                    self.newClues.add(definition)
        print('')

    def preprocess_antonyms(self):
        for antonym in self.antonyms:
            l = antonym.lower()
            for answer in self.answer:
                if l.find(answer.lower()) == -1:
                    new_antonym = 'Opposite of ' + antonym
                    self.newClues.add(new_antonym)
                else:
                    pass

    def preprocess_synonyms(self):
        for synonym in self.synonyms:
            l = synonym.lower()
            for answer in self.answer:
                if l.find(answer.lower()) == -1:
                    self.newClues.add(l)
                else:
                    pass

    def newClueprocess(self):

        print("*" * 10)
        print(self.newClues)

        processed_clues = set()
        for clue in self.newClues:
            clue = clue.lower()
            clue_splitted = clue.split(' ')

            for answer in self.answer:

                word_flag = True

                for c in clue_splitted:
                    if c in answer.lower() or answer.lower() in c:
                        word_flag = False

                if word_flag:
                    processed_clues.add(clue)

        self.newClues = processed_clues

        print("-" * 10)
        print(self.newClues)
