#---------------------------------------------------------------------------------------------
# Wordle 2.0: Clean.py
# Author: Ahmad Olagunju
# February 25, 2022
# Program Description: Takes in corrupted file and cleans it
#---------------------------------------------------------------------------------------------

def main():
    inFile = open("word5Dict.txt", 'r')
    outputFile = open("scrabble5.txt", 'w')
    # print all words - one word per line
    for line in inFile:
        lineList = line.strip("\n").split("#")  # remove newline character and separate words into list
        for word in lineList:
            if word != '':
                outputFile.write(word + "\n")
    inFile.close()
    outputFile.close()


main()
