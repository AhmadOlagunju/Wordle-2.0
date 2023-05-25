#---------------------------------------------------------------------------------------------
# Wordle 2.0: Main.py
# Author: Ahmad Olagunju
# February 25, 2022
# Program Description: Create Wordle 2.0 game using ScrabbleDict class
#---------------------------------------------------------------------------------------------

from Wordle2 import ScrabbleDict
import random


def selectWord(scrabbleList):
    '''
        Return random word from the list of words
        :param: scrabbleList: list of all words
        :return: string: the random word
    '''
    return random.choice(scrabbleList)


def duplicates(word):
    '''
        Return list of duplicates in word
        :param: word: the word to be checked
        :return: duplicatesList: list of the duplicates
    '''
    duplicatesList = []
    # if there is a duplicate in word add it to list
    for letter in word:
        if letter not in duplicatesList and word.count(letter) >= 2:
            duplicatesList.append(letter)
    return duplicatesList


def letterNames(word):
    '''
        Return a list of the letter numberings for the word eg. A1, T2, A
        :param: word: the word to be numbered
        :return: letterNums: a list of the letter names
    '''
    letterNums = list(word)
    duplicatesList = duplicates(word)
    # number the letters in the duplicate list
    for dupLetter in duplicatesList:
        count = 1
        for letterIndex in range(len(word)):
            if word[letterIndex] == dupLetter:
                letterNums[letterIndex] += str(count)
                count += 1
    return letterNums


def playWordle(hiddenWord, scrabbleDict):
    '''
        Simulate wordle175 game
        :param: scrabbleDict: dictionary of words, hiddenWord: the word to be guessed
        :return: N/A
    '''
    hiddenWord = hiddenWord.upper()
    guessedWord = False
    attempts = 1
    guessList = []
    guessLines = []
    # prompt user for guess and output color lists
    while not guessedWord and attempts <= 6:
        guess = guessPrompt(scrabbleDict, guessList, attempts)
        guessList.append(guess)
        green, orange, red = checkGuess(hiddenWord, guess)
        guessedWord = isGuessed(green)
        # format the color lists for output
        guessStr = "" + guess
        colorLists = [green, orange, red]
        colorIndex = 0
        # formatting lists
        for color in ["Green", "- Orange", "- Red"]:
            guessStr += " " + color + "=" + formatList(colorLists[colorIndex])
            colorIndex += 1
        guessLines.append(guessStr)
        for line in guessLines:
            print(line)
        attempts += 1
    if guessedWord:
        print("Found in " + str(attempts - 1) + " attempt(s). Well done. The Word is " + hiddenWord)
    else:
        print("Sorry you lose. The Word is " + hiddenWord)


def guessPrompt(scrabbleDict, guessList, attempts):
    '''
        Prompt user for guess until valid
        :param: guessList: list of previous guesses, scrabbleDict: dict of valid words, attempts: # of attempts
        :return: guess: string of valid guess
    '''
    guess = input("Attempt " + str(attempts) + ": Please enter a 5 five-letter word: ").upper()
    # validate input
    while len(guess) != 5 or scrabbleDict.check(guess) is False or guess in guessList:
        if len(guess) < 5:
            print(guess + " is too short")
        elif len(guess) > 5:
            print(guess + " is too long")
        elif scrabbleDict.check(guess) is False:
            print(guess + " is not a recognized word")
        elif guess in guessList:
            print(guess + " was already entered")
        guess = input("Attempt " + str(attempts) + ": Please enter a 5 five-letter word: ").upper()
    return guess


def isGuessed(greenList):
    '''
        Return whether word is guessed
        :param: greenList: list of letters in correct position
        :return: bool: whether word has been guessed
    '''
    return len(greenList) == 5


def checkGuess(hiddenWord, guess):
    '''
        Return lists that tell color of letters for guess in wordle game
        :param: hiddenWord: secret word, guess: string of user guess
        :return: glist, oList, rList: lists that indicate color of letters in wordle game
    '''
    gList = []
    oList = []
    rList = []
    remainingLetters = list(hiddenWord)
    lName = letterNames(guess)  # list of letter names eg. ALL => A, L1, L2
    # update gList if letter is in correct position
    for letterIndex in range(len(hiddenWord)):
        if guess[letterIndex] == hiddenWord[letterIndex]:
            gList.append(lName[letterIndex])
            remainingLetters[letterIndex] = None
    # update oList and rList depending on whether letter is in word
    for letterIndex in range(len(hiddenWord)):
        if lName[letterIndex] not in gList:
            if guess[letterIndex] in remainingLetters:
                oList.append(lName[letterIndex])
                # update remaining letters when the guess is in the word but at incorrect position
                remainingLetters[remainingLetters.index(guess[letterIndex])] = None
            else:
                rList.append(lName[letterIndex])
    return gList, oList, rList


def formatList(list):
    '''
        Return sorted list with curly brackets
        :param: list: list to be sorted and formatted
        :return: string: formatted and sorted list
    '''
    list.sort()
    return '{' + ', '.join(list) + '}'


def main():
    scrabbleDict = ScrabbleDict(5, "scrabble5.txt")
    hiddenWord = selectWord(scrabbleDict.getAllWords()).upper()
    playWordle(hiddenWord, scrabbleDict)


main()
