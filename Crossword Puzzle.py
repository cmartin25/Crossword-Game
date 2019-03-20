import sys

gridSize = 15


# ~~~~~~~~~~~~~~~~~Defining Functions~~~~~~~~~~~~~~~~~~~
def main():
    puzzle = read_puzzle()
    grid = create_grid(puzzle)
    puzzle_size = len(puzzle.keys())
    guessed_words = 0
    print_grid(puzzle, grid)
    print("Let's play a game!")

    while empty_count(grid) > 0:
        print("(G) Guess Word, (C) Show Clue, (R) Show Grid, (Q) Quit")
        menuChoice = input("Your Choice? ").upper()

        if menuChoice == 'Q':
            print("Thanks for playing!  You guessed " + str(guessed_words) + " out of the " + str(puzzle_size) +
                  " words in the puzzle!\n")

            input("Press ENTER to exit:")
            sys.exit()

        elif menuChoice == 'G':
            guess_box = input("What box number would you like to guess? ")
            guess_direct = input("What direction would you like to guess in? ")
            foundWord = find_word(puzzle, guess_box, guess_direct)
            if foundWord == None:
                print("This is not a valid location.")
            elif foundWord != None:
                guessword = foundWord["word"]
                player_guess = input("Please guess the word. ").upper()
                if player_guess == guessword:
                    add_word(foundWord, grid)
                    guessed_words += 1

                    print("Your guess was correct!")
                else:
                    print("Your guess was incorrect.")

        elif menuChoice == 'C':
            clue_box = input("What box number would you like the clue to be from? ")
            clue_direct = input("What direction do you need the clue for? ")
            wordclue = find_word(puzzle, clue_box, clue_direct)
            if wordclue == None:
                print("This is not a valid location.")
            if wordclue != None:
                clue_phrase = wordclue["clue"]
                print(clue_phrase)

        elif menuChoice == 'R':
            print_grid(puzzle, grid)
        else:
            print("I'm sorry, but I don't recognize that option.  Please try again.\n")

    print("\n*** CONGRATULATIONS, YOU GUESSED ALL THE WORDS! ***\n")
    input("\nThanks for a stimulating game!  Press ENTER to exit:")

    sys.exit()


# ----------------------------------------
def read_puzzle():
    inputFile = open("puzzle.csv")
    puzzle = {}
    line = inputFile.readline()

    while len(line) > 0:
        line = line.strip()
        wordlist = line.strip("\"").strip(",").split('\t')
        newWord = {}

        newWord["y"] = int(wordlist[0])
        newWord["x"] = int(wordlist[1])
        newWord["box"] = int(wordlist[2])
        newWord["direction"] = wordlist[3]
        newWord["word"] = wordlist[4]
        newWord["clue"] = wordlist[5]

        key_name = wordlist[3] + wordlist[2]
        puzzle[key_name] = newWord
        line = inputFile.readline()
    inputFile.close()

    return puzzle


# ----------------------------------------
def create_grid(puzzle):
    grid = [['*' for x in range(gridSize)] for x in range(gridSize)]

    for key in puzzle:
        word = puzzle[key]
        list_word = list(word["word"])
        x = word["x"]
        y = word["y"]

        for letter in list_word:
            grid[y][x] = ' '
            if word["direction"] == "A":
                x = x + 1

            elif word["direction"] == "D":
                y = y + 1

    return grid


# ----------------------------------------
def add_word(newWord, grid):
    listWord = list(newWord["word"])
    x = newWord["x"]
    y = newWord["y"]

    for letter in listWord:
        grid[y][x] = letter
        if newWord["direction"] == "A":
            x = x + 1
        elif newWord["direction"] == "D":
            y = y + 1


# ----------------------------------------
def csv_write(word):
    file = open('guessedwords.csv', 'a')
    file.write(str(word['box'])+'\t'+word['direction'] + '\n')
    file.close()


# ----------------------------------------
def find_word(puzzle, box, direction):
    keyName = direction.upper() + str(box)
    word = puzzle.get(keyName)

    return word


# ----------------------------------------
def empty_count(grid):
    counter = 0
    for row in grid:
        for column in row:
            if column == ' ':
                counter += 1

    return counter


# ----------------------------------------
def print_grid(puzzle, grid):
    boxNumbers = [[0 for x in range(gridSize)] for x in range(gridSize)]

    for key in puzzle:
        next_word = puzzle[key]
        x = int(next_word['x'])
        y = int(next_word['y'])
        box = int(next_word['box'])
        boxNumbers[y][x] = box

    for y in range(0, gridSize):
        for x in range(0, gridSize):
            if boxNumbers[y][x] == 0:
                sys.stdout.write('+---')
            elif boxNumbers[y][x] < 10:
                sys.stdout.write('+-' + str(boxNumbers[y][x]) + '-')
            elif boxNumbers[y][x] >= 10:
                sys.stdout.write('+' + str(boxNumbers[y][x]) + '-')
        sys.stdout.write('+\n|')

        for x in range(0, gridSize):
            sys.stdout.write(' ' + grid[y][x] + ' |')
        sys.stdout.write("\n")

    print('+' + '---+' * gridSize)


# ~~~~~~~~~~~~~~~~~~~~Execution~~~~~~~~~~~~~~~
main()
