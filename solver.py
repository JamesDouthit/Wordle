import sys
import string
import copy

def processNewInfo(guessable_map,new_guess,secret):
    """Populate the board with a new guess."""
    # could/should make this just read from the file since nothing else needs to
    # secrets_set = "./secret.txt"
    new_board_state = copy.deepcopy(guessable_map)
    # keep track so we dont double count letters
    letter_counts = {}
    for letter in new_guess:
        letter_counts[letter] = letter_counts.get(letter,0)+1
    for letter_pos in range(len(new_guess)):
        letter = new_guess[letter_pos]
        # letter is not in secret
        if letter not in secret:
            new_board_state[letter] = {}
        # letter is in the right place
        elif secret.find(letter) == letter_pos or secret.rfind(letter) == letter_pos:
            # remove that position from all letters
            for letter_pos_set in new_board_state.values():
                letter_pos_set.discard(str(letter_pos))
            # just the correct letter goes in that position
            new_board_state[letter].add(str(letter_pos))
            #account for the letter
            letter_counts[letter] = letter_counts.get(letter,0)-1
        # letter in secret, but wrong place
        elif letter_counts[letter]>0:
            new_board_state[letter].discard(str(letter_pos))
            # account for the letter
            letter_counts[letter] = letter_counts.get(letter,0)-1            
    return new_board_state

def rateGuessLetter(occurrences, space_size):
    """Rate a letter based on how close it comes to dividing the space in 2."""
    raw_fraction = occurrences/space_size
    return abs(0.5-raw_fraction)

def findCommonLetters(guess_words):
    """Count number of times letters occur in given guess words."""
    letter_occurrences = dict.fromkeys(list(string.ascii_lowercase))
    for word in guess_words:
        letters_used = ""
        for letter in word:
            if letter not in letters_used:
                letter_occurrences[letter] = letter_occurrences.get(letter,0) + 1
                letters_used.append(letter)
    return letter_occurrences

def findBestGuess(poss_guess_words):
    """Given a list of possible guesses, choose the one that if chosen maximizes eliminations."""
    letter_occurrences = findCommonLetters(poss_guess_words)
    word_ratings = dict.fromkeys(poss_guess_words)
    guess_space_size = len(poss_guess_words)
    for guess_word in poss_guess_words:
        letters_used = ""
        for letter in guess_word:
            if letter not in letters_used:
                word_ratings[guess_word] = word_ratings[guess_word] + \
                    rateGuessLetter(letter_occurrences[letter],guess_space_size)
    # for potential_best_word, word_rating in word_ratings.items():
    best_guess_word = max(word_ratings, key=word_ratings.get)
    return best_guess_word

def trimPossGuesses(board_state, curr_guess_set):
    """Given a board, exclude the guesses that can no longer be the secret."""
    if len(board_state == 0):
        return curr_guess_set
    new_guess_set = copy.deepcopy(curr_guess_set)
    for word in curr_guess_set:
        for letter_pos in range(len(word)):
            letter = word[letter_pos]
            if str(letter_pos) not in board_state[letter]:
                new_guess_set.remove(word)
                break
    return new_guess_set

def executeTurn(board_state, poss_guesses, secret):
    """Make a guess and populate the board with it."""
    new_poss_guesses = trimPossGuesses(board_state, poss_guesses)
    best_guess = findBestGuess(new_poss_guesses)
    print("guessed",best_guess)
    new_board_state = processNewInfo(board_state, best_guess, secret)
    if(best_guess == secret):
        return True, new_board_state, new_poss_guesses
    return False, new_board_state, new_poss_guesses

def solveGivenSecret(given_secret):
    """Auto-solve through all turns for a given secret."""
    f = open("secret.txt", "r")
    secrets_set = set(f.readlines())
    if given_secret not in secrets_set:
        print("That isn't a possible secret")
    f = open("guess.txt", "r")
    guesses = set(f.readlines())
    state = dict.fromkeys(list(string.ascii_lowercase))
    turns_taken = 0
    while True:
        turns_taken += 1
        done, state, guesses  = executeTurn(state, guesses, given_secret)
        # state = new_state
        # guesses = pared_guesses
        if done:
            break
    print("Found",given_secret,"in",turns_taken,"turns!")
    return

if __name__ == "__main__":
    secret = sys.argv[1]
    solveGivenSecret(secret)
    # # not related to solver
    # mytest = {'black':dict.fromkeys(list(string.ascii_lowercase))}
    # # end not related to solver
