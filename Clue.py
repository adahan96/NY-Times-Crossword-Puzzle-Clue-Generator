import random
import spacy
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process
from Finders.DatamuseFinder import findFromDatamuse
from Finders.MerriamWebsterFinder import findFromMWDictionary, findFromMWThesaurus
from Finders.Wordnet import findFromWordnet
from Finders.UrbanDictionaryFinder import findFromUrbanDictionary
from GoogleSearch import getDidyoumeanSuggestion


class Clue:
    def __init__(self, originalClue, answer):
        self.originalClue = originalClue
        self.originalAnswer = answer.lower()
        self.answers = set()  # The set contains the original answer and alternative answesr
        self.answers.add(self.originalAnswer)
        self.findAlternativeAnswers()

        """New clues is a list of 3-tuples: (clue, category, source)
        Categories: synonym
        Sources: datamuse
        """
        self.newClues = []  # Not a set because new clues will be sorted later
        self.definitions = set()
        self.synonyms = set()
        self.antonyms = set()
        self.example_sentences = set()

        # Initialization
        self.nlp = spacy.load('en_core_web_sm')

    def findAlternativeAnswers(self):
        """Find alternative answers and add them to answers set
        """
        corrected_answer = getDidyoumeanSuggestion(self.originalAnswer)
        if corrected_answer is not None:
            self.answers.add(corrected_answer)

    def generateNewClues(self):
        run_io_tasks_in_parallel([
            self.findFromWordnet,
            self.searchDatamuse,
            self.findFromMWDictionary,
            self.findFromMWThesaurus,
            self.findUrbanDictionary
        ])
        self.preprocess_clues()
        self.filterNewClues()
        self.sortNewClues()
        print('\n'.join(map(str, self.newClues)))  # Print sorted clues

    def filterNewClues(self):
        """New clues that contain any answer (original or alternative) and that are similar to
        original clue should be removed from newClues list
        """
        # Remove clues that contain original answer
        # TODO: This part should be fixed
        """
        for clue in self.newClues:
            clueWords = clue[0].lower().split(' ')

            for answer in self.answers:
                for c in clueWords:
                    if c in answer.lower() or answer.lower() in c:
                        self.newClues.remove(clue)
        """
        # Remove similar clues
        threshold = 0.80

        originalClue_nlp = self.nlp(self.originalClue)
        filteredClues = set()
        for clue in self.newClues:
            similarity_percent = originalClue_nlp.similarity(self.nlp(clue[0]))
            if similarity_percent >= threshold:
                self.newClues.remove(clue)

    def getTheBestClue(self):
        if len(self.newClues) != 0:
            return self.newClues[0][0]
        else:
            print(
                f"Error: newClues is empty for the answer {self.originalAnswer}")
            return None

    def getRandomNewClue(self):
        if len(self.newClues) != 0:
            return random.choice(list(self.newClues))
        else:
            return None

    def findFromWordnet(self):
        for answer in self.answers:
            antonym, definition, exampleSentence = findFromWordnet(answer)
            if antonym is not None:
                self.antonyms.add((antonym, "wordnet"))
            if definition is not None:
                self.definitions.add((definition, "wordnet"))
            if exampleSentence is not None:
                self.example_sentences.add((exampleSentence, "wordnet"))

    def searchDatamuse(self):
        """Datamuse results are added to synonyms
        """
        for answer in self.answers:
            result = findFromDatamuse(answer)
            if result is not None:
                self.synonyms.add((result, "datamuse"))

    def findFromMWDictionary(self):
        for answer in self.answers:
            definition, sentence = findFromMWDictionary(answer)
            if definition is not None:
                self.definitions.add((definition, "mw"))
            if sentence is not None:
                self.example_sentences.append((sentence, "mw"))

    def findFromMWThesaurus(self):
        for answer in self.answers:
            synonym, antonym = findFromMWThesaurus(answer)
            if synonym is not None:
                self.synonyms.add((synonym, "mw"))
            if antonym is not None:
                self.antonyms.add((antonym, "mw"))

    def findUrbanDictionary(self):
        for answer in self.answers:
            meaning, example = findFromUrbanDictionary(answer)
            if meaning is not None:
                self.definitions.add((meaning, "urban"))
            if example is not None:
                self.example_sentences.add((example, "urban"))

    def preprocess_clues(self):
        # TODO: These steps can be parallelized for a faster computation
        self.preprocess_example_sentences()
        self.preprocess_antonyms()
        self.preprocess_synonyms()
        self.preprocess_definitions()

    def preprocess_example_sentences(self):
        """For every example sentence, replace answer with ___
        and add (sentence, "example-sentence", source) tuple to newClues
        """
        max_word_number = 13
        for answer in self.answers:
            for exs in self.example_sentences:
                exampleSentence, source = exs[0], exs[1]
                if answer.lower() in exampleSentence and len(exampleSentence.split(' ')) < max_word_number:
                    newExampleSentence = exampleSentence.replace(
                        answer.lower(), '___')
                    self.newClues.append(
                        (newExampleSentence, "example-sentence", source))

    def preprocess_definitions(self):
        max_word_number = 13
        for definition in self.definitions:
            for answer in self.answers:
                definition, source = definition[0], definition[1]
                if len(definition.split(' ')) < max_word_number and answer.lower() not in definition.lower():
                    self.newClues.append((definition, "definition", source))

    def preprocess_antonyms(self):
        for antonym in self.antonyms:
            antonym, source = antonym[0], antonym[1]
            l = antonym.lower()
            for answer in self.answers:
                if l.find(answer.lower()) == -1:
                    new_antonym = 'Opposite of ' + antonym
                    self.newClues.append((new_antonym, "antonym", source))

    def preprocess_synonyms(self):
        for synonym in self.synonyms:
            synonym, source = synonym[0], synonym[1]
            l = synonym.lower()
            for answer in self.answers:
                if l.find(answer.lower()) == -1:
                    self.newClues.append((l, "synonym", source))

    def sortNewClues(self):
        sourceSorting = [
            "wordnet",
            "mw",
            "datamuse",
            "urban"
        ]

        categorySorting = [
            "definition",
            "synonym",
            "antonym",
            "example-sentence"
        ]

        try:
            self.newClues = sorted(self.newClues, key=lambda x: (
            sourceSorting.index(x[2]), categorySorting.index(x[1])))
        except:
            pass

def run_io_tasks_in_parallel(tasks):
    # https://stackoverflow.com/a/56138825/5964489
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            running_task.result()


def run_cpu_tasks_in_parallel(tasks):
    # https://stackoverflow.com/a/56138825/5964489
    running_tasks = [Process(target=task) for task in tasks]
    for running_task in running_tasks:
        running_task.start()
    for running_task in running_tasks:
        running_task.join()
