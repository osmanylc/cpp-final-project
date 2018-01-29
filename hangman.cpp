#include <fstream>
#include <iostream>
#include <sstream>
#include <map>
#include <vector>
#include <math.h>
#include <algorithm>
//#include <stdlib>
#include <cstdlib>
#include <ctime>

std::vector<std::string> wordList;

void loadWords(){
  //make a list of valid words where the words are all strings of lowercase letters.
  //i.e. read in words from words.txt file and store them in wordList vector

  std::cout << "Loading word list from file..." << std::endl;
  std::ifstream wordsFile("words.txt");

  while (wordsFile) {
    std::string inputWord;
    wordsFile >> inputWord;
    wordList.push_back(inputWord);
  }
}

std::string chooseWord(std::vector<std::string> words){
  //pick a random word from the wordlist returned from loadwords (i.e. from wordList) and return it
  srand(static_cast<unsigned int>(time(0)));
  int index = rand() % words.size();

  return words[index];
}

bool wordGuessed(std::string wordToGuess, std::vector<char> guessedLetters){
  //wordToGuess: the word that the user is supposed to guess
  //guessedLetters: vector of letters user has guessed so far
  //return True if all letters in wordToGuess are also in guessedLetters
  for(int i = 0; i < wordToGuess.size(); i++) {
    bool isLetterGuessed = false;
    for(int j = 0; j < guessedLetters.size(); j++) {
      if (wordToGuess[i] == guessedLetters[j]) {
        isLetterGuessed = true;
      }
    }
    if (!isLetterGuessed) {
      return false;
    }
  }
  return true;
}

std::string getGuessedWord(std::string wordToGuess, std::vector<char> guessedLetters){
  //wordToGuess: the word that the user is supposed to guess
  //guessedLetters: vector of letters user has guessed so far
  //return: string representing the currently guessed word in format where any correctly guessed letters from the
  //  word to guess are in their correct places and any letters that haven't been guessed are represented by _
  //  e.g. if word is "hello" and "e" and "o" have been guessed, this function would return "_e__o"
  std::string guessedWord = "";
  for(int i = 0; i < wordToGuess.size(); i++) {
    bool isLetterGuessed = false;
    for(int j = 0; j < guessedLetters.size(); j++) {
      if (wordToGuess[i] == guessedLetters[j]) {
        isLetterGuessed = true;
      }
    }
    if (isLetterGuessed) {
      guessedWord = guessedWord + wordToGuess[i];
    } else {
      guessedWord = guessedWord + "_";
    }
  }
  return guessedWord;
}

std::string getAvailLetters(std::vector<char> guessedLetters){
  //guessedLetters: vector of letters user has guessed so far
  //return string of letters that the user hasn't guessed yet
  std::string availLetters = "";
  std::string letters = "abcdefghijklmnopqrstuvwxyz";
  for(char& c : letters) {
    if (std::find(guessedLetters.begin(), guessedLetters.end(), c) == guessedLetters.end())
    {
      availLetters += c;
    }
  }

  return availLetters;
}

int getScore(std::string wordToGuess, int guessesLeft){
  //wordToGuess: the word that the user is supposed to guess
  //guessesLeft: number of guesses user has left
  //return score, where score = guessesLeft + # unique letters in wordToGuess + len of wordToGuess
    std::vector<char> unique_letters = std::vector<char>(wordToGuess.begin(), wordToGuess.end());
    std::sort(unique_letters.begin(), unique_letters.end());
    // returns an iterator to the element that follows the last element not removed
    auto new_last = std::unique(unique_letters.begin(), unique_letters.end());
    unique_letters.erase(new_last, unique_letters.end());
    return guessesLeft + unique_letters.size() + wordToGuess.length();
}

char getRandomLetter(std::string wordToGuess, std::string availLetters){
  //return a random letter that is in wordToGuess that HASN'T been guessed yet
    std::vector<char> unguessed;
    std::stringstream ss;
    for (char& c : availLetters) {
        std::string s;
        ss << c;
        ss >> s;
        if (s.find_first_of(wordToGuess) != std::string::npos) {
            unguessed.push_back(c);
        }
    }
    int index = rand() % unguessed.size()+1;  //EDIT: idk if inclusive of the maxval or not?
    return unguessed.at(index);             //EDIT: should I return it as a character or as a string
}

int main(){
  /*
   Starts up an interactive game of Hangman.

   * At the start of the game, let the user know how many
     letters the secret_word contains and how many guesses s/he starts with.

   * The user should start with 10 guesses

   * Before each round, you should display to the user how many guesses
     s/he has left and the letters that the user has not yet guessed.

   * Ask the user to supply one guess per round. Make sure to check that the user guesses a valid letter!

   * The user should receive feedback immediately after each guess
     about whether their guess appears in the computer's word.

   * After each guess, you should display to the user the
     partially guessed word so far.

   * If the guess is the symbol #, you should reveal to the user one of the
     letters missing from the word at the cost of 2 guesses. If the user does
     not have 2 guesses remaining, print a warning message. Otherwise, add
     this letter to their guessed word and continue playing normally.

  More rules/what to do:
     1. If the user inputs anything besides an alphabet (symbols, numbers), tell the user
     that they can only input a letter in the alphabet.
     2. If the user inputs a letter that has already been guessed, print a message telling
     the user the letter has already been guessed before.
     3. If the user inputs a letter that hasn’t been guessed before and the letter is in the
     secret word, the user loses no​ guesses.
     4. Consonants:​ If the user inputs a consonant that hasn’t been guessed and the
     consonant is not in the secret word, the user loses one​ guess if it’s a consonant.
     5. Vowels:​ If the vowel hasn’t been guessed and the vowel is not in the secret word,
     the user loses two​ guesses.
     6. The game should end when the user constructs the full word or runs out of
     guesses.
     7. If the player runs out of guesses before completing the word, tell them they lost
     and reveal the word to the user when the game ends.
     8. If the user wins, print a congratulatory message and tell the user their score. */

  loadWords();
  std::string secretWord = chooseWord(wordList);
  int guessesLeft = 10;
  bool used = false; //true when free letter is used
  std::string validLetters = "abcdefghijklmnopqrstuvwxyz";
  std::string vowels = "aeiou";
  std::vector<char> lettersGuessed;
  char guess;
  std::string availLetters=validLetters;

  std::cout << "Welcome to Hangman! The word that I am thinking of is " << secretWord.length() << " letters long." << std::endl;

  while(guessesLeft>0){
    std::cout << "You have " << guessesLeft << " guesses left." << std::endl;
    std::cout << "Your currently guessed word is: " << getGuessedWord(secretWord, lettersGuessed) << std::endl;
    availLetters=getAvailLetters(lettersGuessed);
    std::cout << "Your available letters are: " << availLetters << std::endl;

    std::cin >> guess;

    if(guess=='!'){ //end game. not mentioned in game rules but it's useful to be able to quit the game easily
      break;
    }

    else if(guess=='#'){ //user wants to reveal a letter
      if(guessesLeft > 2){
        char letter = getRandomLetter(secretWord, availLetters);
        lettersGuessed.push_back(letter);
        guessesLeft-=2;
        std::cout << "Letter revealed: " << letter << std::endl;
      }
      else{
        while(guessesLeft < 2 && guess=='#'){
          std::cout << "You don't have enough guesses available to use a hint! Please enter in a guess: " << std::endl;
          std::cin >> guess;
        }
      }
    }

    else if(validLetters.find_first_of(guess)==std::string::npos){
      std::cout << "That is not a valid letter." << std::endl;
    }

    else if(std::find(lettersGuessed.begin(),lettersGuessed.end(),guess)!=lettersGuessed.end()){
      std::cout << "You have already guessed that letter." << std::endl;
    }

    else if(secretWord.find_first_of(guess)!=std::string::npos){
      lettersGuessed.push_back(guess);
      std::cout << "Good guess!" << std::endl;
    }

    else if(secretWord.find_first_of(guess)==std::string::npos){
      lettersGuessed.push_back(guess);
      std::cout << "Sorry, that letter is not in my word." << std::endl;

      if(vowels.find_first_of(guess)!=std::string::npos){
        guessesLeft-=2;
      }
      else{
        guessesLeft-=1;
      }
    }

    std::cout << "Your current guessed word is: " << getGuessedWord(secretWord, lettersGuessed) << std::endl;

    if(wordGuessed(secretWord, lettersGuessed)==true){
      break;
    }

    std::cout << std::endl;
  }

  if(wordGuessed(secretWord, lettersGuessed)==true){
    std::cout << "Congrats! You won the game. Your score is: " << getScore(secretWord, guessesLeft) << std::endl;
  }

  else{
    std::cout << "You lost. Better luck next time!" << std::endl;
  }

  return 0;
}
