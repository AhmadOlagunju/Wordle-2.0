#---------------------------------------------------------------------------------------------
# Wordle 2.0: Wordle2.py
# Author: Ahmad Olagunju
# February 25, 2022
# Program Description: ScrabbleDict class for wordle 2.0 game
#---------------------------------------------------------------------------------------------

class ScrabbleDict:
    def __init__(self, size, fileName):
        assert isinstance(size, int), (
                'Error: Type error: %s' % (type(size)))  # throws an assertion error on not true
        assert size > 0, ('Error: Invalid word size: %d' % (size))

        inFile = open(fileName, 'r')
        self.scrabbleDict = {}
        self.wordSize = size
        # first element in line is the key for the dictionary, the full line is the value
        for line in inFile:
            word = line.split()[0]
            if len(word) == self.wordSize:
                self.scrabbleDict[word] = line.strip("\n")
        inFile.close()

    def check(self, word):
        """
            Check if the word exists in the dictionary
            :param: word: the word to be checked
            :return: bool: whether the word is in the dictionary
        """
        return word.lower() in self.scrabbleDict

    def getSize(self):
        """
            Get the size of the dictionary
            :param: N/A
            :return: int: size of the dictionary
        """
        return len(self.scrabbleDict)

    def getWords(self, letter):
        """
            Return all words that start with given letter
            :param: letter: letter that words should start with
            :return: list: sorted words that start with given letter
        """
        words = []
        for word in sorted(self.scrabbleDict):
            if word[0] == letter:
                words.append(word)
        return words

    def getWordSize(self):
        """
            Get the size of words in the dictionary
            :param: N/A
            :return: int: size of words in the dictionary
        """
        return self.wordSize

    def getAllWords(self):
        """
            Returns all words in the dictionary
            :param: N/A
            :return: list: all words in the dictionary
        """
        return list(self.scrabbleDict.keys())

    def getMaskedWords(self, template):
        """
            Returns all words in the dictionary that follow template
            :param: template: string containing wildcards
            :return: hints: a list of words in the dictionary that follow the template
        """
        assert len(template) == self.wordSize, "Error: Invalid template"
        hints = []
        template = template.lower()
        # append to list if word follows template
        for word in self.scrabbleDict:
            isHint = True
            i = 0
            while isHint and i < len(word):
                if template[i] != '*' and template[i] != word[i]:
                    isHint = False
                i += 1
            if isHint:
                hints.append(word)
        return hints

    def getConstrainedWords(self, template, letters):
        """
            Returns all words in the dictionary that follow template and contain given letters
            :param: template: string containing wildcards, letters: list of characters that should be in each word
            :return: constrained: a list of words that follow the template and contain given letters
        """
        assert len(template) == self.wordSize, "Error: Invalid template"
        assert len(letters) <= template.count('*'), "Error: Invalid list of letters (More letters than wildcards)"
        hintList = self.getMaskedWords(template)
        constrained = []
        template = template.lower()
        # if there are no wildcards then use maskedWords
        if template.count('*') > 0:
            # find possible spots for letters based on wildcards
            fWildcardIndex = template.index('*')
            lWildcardIndex = template.rfind('*')
            # check if word has letters in correct frequency eg. if letters is [i,i] word must have 2 i's
            for word in hintList:
                hasLetters = True
                possibleSpots = word[fWildcardIndex: lWildcardIndex + 1]
                sameFrequency = True
                i = 0
                while i < len(letters) and hasLetters:
                    if letters[i].lower() not in possibleSpots:
                        hasLetters = False
                    i += 1
                if hasLetters:
                    for letter in letters:
                        if possibleSpots.count(letter.lower()) < letters.count(letter):
                            sameFrequency = False
                    if sameFrequency:
                        constrained.append(word)
        else:
            return hintList
        return constrained


if __name__ == "__main__":

    # test whether instance is created without error
    scrabbleDict = ScrabbleDict(5, 'scrabble5.txt')

    # test - try to make word length 0
    try:
        print("Making word size 0: ")
        scrabbleDict = ScrabbleDict(0, 'scrabble5.txt')
    except Exception as lengthError:
        print(lengthError.args)

    # test getWordSize function
    print("\nTesting getWordSize(): ", scrabbleDict.getWordSize(), sep="")

    # test check function
    print("\nTesting check(): ")
    print("Testing 'Trunk': ", scrabbleDict.check("Trunk"))
    print("Testing 'little': ", scrabbleDict.check("little"))
    print("Testing '':", scrabbleDict.check(""))

    # test getSize function
    print("\nTesting getSize(): ", scrabbleDict.getSize())

    # test getWords function
    print("\nTesting getWords('a'): ", scrabbleDict.getWords('a'))
    print("Testing getWords(''): ", scrabbleDict.getWords(''))

    # test getAllWords function
    print("\nTesting getAllWords():\n", scrabbleDict.getAllWords(), sep="")

    # test getMaskedWords function
    try:
        print("\nTesting getMaskedWords(): ")
        print("Testing 't**er': ", scrabbleDict.getMaskedWords("t**er"))
        print("Testing '*****': ", scrabbleDict.getMaskedWords("*****"))
        print("Testing 't**err': ")
        print(scrabbleDict.getMaskedWords("t**err"))
    except Exception as templateError:
        print(templateError.args)

    # test getConstrainedWords function
    try:
        print("\nTesting getConstrainedWords('t**er', ['i']):", scrabbleDict.getConstrainedWords("t**er", ['i']))
        print("\nTesting getConstrainedWords('t**er', ['i', 'i']):",
              scrabbleDict.getConstrainedWords("t**er", ['i', 'i']))
        print("\nTesting getConstrainedWords('t**er', ['i', 'i', 'i']):")
        print(scrabbleDict.getConstrainedWords("t**er", ['i', 'i', 'i']))
    except Exception as constrainedError:
        print(constrainedError.args)
