# Problem Set 2, hangman.py
# Name: Christine Vonder Haar
# Collaborators: N/A
# Time spent: 1.5 - 2 hours

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters and octothorps (_) that represents
      which letters in secret_word have been guessed so far.
    '''
    word = ""
    for letter in secret_word:
        if letter in letters_guessed:
            word += letter
        else:
            word += '_'
    return word



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which 
      letters have not yet been guessed.
    '''
    available_letters = ""
    for letter in string.ascii_lowercase:
        if letter not in letters_guessed:
            available_letters += letter
    return available_letters


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 10 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    guesses_remaining = 10
    warnings_remaining = 4
    available_letters = string.ascii_lowercase
    letters_guessed = []
    vowels = "aeiou"

    print("Welcome to Hangman! \nI am thinking that is", str(len(secret_word)), "letters long")
    print("You have", warnings_remaining, "warnings left")
    print("----------------------------------------------------------")

    while guesses_remaining > 0:
        # intro for each guess
        guesses_string = "guess" if guesses_remaining == 1 else "guesses"
        print("You have", guesses_remaining, guesses_string, "left.")
        print("Available letters:", get_available_letters(letters_guessed))
        character = input("Please guess a letter: ").lower()

        if character == '!':
            break;

        if not character.isalpha() or character in letters_guessed:
            if not character.isalpha():
                print("Oops! That is not a valid letter. ", end="")
            elif character in letters_guessed:
                print("Oops! You already guessed that letter. ", end="")

            if warnings_remaining == 0:
                guesses_remaining -= 1
                print("You had no warnings left so you lost a guess", end="")
            else:
                warnings_remaining -= 1
                warnings_string = "warning" if warnings_remaining == 1 else "warnings"
                print("You have", warnings_remaining, warnings_string, "left", end="")
        elif character in secret_word:
            letters_guessed.append(character)
            print("Good guess", end="")
        else:
            print("Oops! That letter is not in my word", end="")
            if character in vowels:
                guesses_remaining -= 2
            else:
                guesses_remaining -= 1
            letters_guessed.append(character)



        print(": ", get_guessed_word(secret_word, letters_guessed))
        print("----------------------------------------------------------")
        if is_word_guessed(secret_word, letters_guessed):
            break;

    # check if won, print appropriate message
    if is_word_guessed(secret_word, letters_guessed):
        print("Congratulations, you won! \nYour total score for this game is", str(get_score(secret_word, guesses_remaining)))
    else:
        print("Sorry, you ran out of guesses. The word was", secret_word,".")

def get_score(secret_word, guesses_remaining):
    unique_letters = set(list(secret_word))
    return guesses_remaining + len(unique_letters) * len(secret_word)

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def hangman_with_help(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 10 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol #, you should reveal to the user one of the 
      letters missing from the word at the cost of 2 guesses. If the user does 
      not have 2 guesses remaining, print a warning message. Otherwise, add 
      this letter to their guessed word and continue playing normally.
      
    * If the guess is the symbol *, you should randomly select one of the 
      available letters and add it to the set of guessed letters at no extra
      cost. This can only be done once per game.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    dashes = "----------------------------------------------------------"
    guesses_remaining = 10
    warnings_remaining = 4
    free_used = False
    available_letters = string.ascii_lowercase
    letters_guessed = []
    vowels = "aeiou"

    print("Welcome to Hangman! \nI am thinking that is", str(len(secret_word)), "letters long")
    print("You have", warnings_remaining, "warnings left")
    print(dashes)

    while guesses_remaining > 0:
        # intro for each guess
        guesses_string = "guess" if guesses_remaining == 1 else "guesses"
        available_letters = get_available_letters(letters_guessed)
        print("You have", guesses_remaining, guesses_string, "left.")
        print("Available letters:", available_letters)
        character = input("Please guess a letter: ").lower()

        if character == '!':
            break;
        elif character == '#':
            while guesses_remaining < 2 and character == '#':
                character = input("You don't have enough guesses to use a hint! Please retry: ")  
            else:
                revealed_letter = get_random_letter(secret_word, get_available_letters(letters_guessed))
                letters_guessed.append(revealed_letter)
                guesses_remaining -= 2
                print("Letter revealed:", revealed_letter)
                print("Secret word", end="")
        elif character == '*':
            if free_used:
                print("You have already used your free guess")
                print(dashes)
                continue
            else:
                index = random.randint(0, len(available_letters) -1)
                free_char = available_letters[index]
                free_used = True
                print("You used your free guess on the letter", free_char)
                if free_char in secret_word:
                    letters_guessed.append(free_char)
                    print("That letter was in the secret word", end="")
                else:
                    print("Sorry, that letter wasn't in the secret word", end="")
                letters_guessed.append(free_char)
        elif not character.isalpha() or character in letters_guessed:
            if not character.isalpha():
                print("Oops! That is not a valid letter. ", end="")
            elif character in letters_guessed:
                print("Oops! You already guessed that letter. ", end="")

            if warnings_remaining == 0:
                guesses_remaining -= 1
                print("You had no warnings left so you lost a guess", end="")
            else:
                warnings_remaining -= 1
                warnings_string = "warning" if warnings_remaining == 1 else "warnings"
                print("You have", warnings_remaining, warnings_string, "left", end="")

        elif character in secret_word:
            letters_guessed.append(character)
            print("Good guess", end="")
        else:
            print("Oops! That letter is not in my word", end="")
            if character in vowels:
                guesses_remaining -= 2
            else:
                guesses_remaining -= 1
            letters_guessed.append(character)



        print(": ", get_guessed_word(secret_word, letters_guessed))
        print(dashes)
        if is_word_guessed(secret_word, letters_guessed):
            break;

    # check if won, print appropriate message
    if is_word_guessed(secret_word, letters_guessed):
        print("Congratulations, you won! \nYour total score for this game is", str(get_score(secret_word, guesses_remaining)))
    else:
        print("Sorry, you ran out of guesses. The word was", secret_word)


def get_random_letter(secret_word, available_letters):
    rand_letter = ''
    while rand_letter == '' or rand_letter not in available_letters:
        index = random.randint(0, len(secret_word) -1)
        rand_letter = secret_word[index]
    return rand_letter

# When you've completed your hangman_with_help function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = "hi"
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_help(secret_word)
