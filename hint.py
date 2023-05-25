#---------------------------------------------------------------------------------------------
# Wordle 2.0: Hint.py
# Author: Ahmad Olagunju
# February 25, 2022
# Program Description: hints for wordle 2.0 game
#---------------------------------------------------------------------------------------------

from Wordle2 import ScrabbleDict


def frequencyDict(matchingWords):
    assert len(matchingWords) > 0, "No matching words cannot graph"
    freqDict = {}
    for word in matchingWords:
        for letter in word:
            if letter in freqDict:
                freqDict[letter] += 1
            else:
                freqDict[letter] = 1
    return freqDict


def graphFreq(matchingWords):
    freqDict = frequencyDict(matchingWords)
    totalNumOfLetters = 0
    for value in freqDict.values():
        totalNumOfLetters += value
    for letter in sorted(freqDict):
        freqStr = ""
        letterPercent = freqDict[letter] / totalNumOfLetters * 100
        percentStr = "{:.2f}%".format(letterPercent)
        graphStr = '*' * round(letterPercent)
        freqStr += letter.upper() + ": {:>4.4} {:>6}  {:}".format(str(freqDict[letter]), percentStr, graphStr)
        print(freqStr)


def main():
    scrabbleDict = ScrabbleDict(5, "scrabble5.txt")
    template = input("Please enter a 5 character template: ")
    while len(template) != 5:
        template = input("Invalid template length! Please enter a 5 character template: ")
    moreLetters = list(input("Please enter additional letters or click enter: "))
    try:
        if len(scrabbleDict.getConstrainedWords(template, moreLetters)) == 0:
            print("No matching words.")
        else:
            print("\nMatching Words: \n" + str(scrabbleDict.getConstrainedWords(template, moreLetters)))
    except Exception as templateError:
        print(templateError.args)

    try:
        print("\nFrequency of letters in template list: ")
        graphFreq(scrabbleDict.getConstrainedWords(template, moreLetters))
    except Exception as graphError:
        print(graphError.args)
    print("\nFrequency of all letters in the file: ")
    graphFreq(scrabbleDict.getMaskedWords("*****"))


main()
