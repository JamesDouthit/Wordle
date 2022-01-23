import sys
import string
import copy
import time

def letterCorrectlyPlaced(checking_letter,checking_letter_position,checking_secret):
    """Checks if a letter is in the right place."""
    if not checking_letter in checking_secret:
        return False
    for secret_letter_position in range(len(checking_secret)):
        if checking_letter == checking_secret[secret_letter_position] and checking_letter_position == secret_letter_position:
            return True
    return False

def processNewInfo(guessable_map,new_guess,secret):
    """Populate the board with a new guess."""
    # could/should make this just read from the file since nothing else needs to
    # secrets_set = "./secret.txt"
    new_board_state = copy.deepcopy(guessable_map)
    # keep track so we dont double count letters
    letter_counts = dict()
    for letter in new_guess:
        letter_counts[letter] = letter_counts.get(letter,0)+1
    for letter_pos in range(len(new_guess)):
        letter = new_guess[letter_pos]
        # letter is not in secret
        if letter not in secret:
            new_board_state[letter] = set()
        # letter is in the right place
        elif letterCorrectlyPlaced(letter,letter_pos,secret):
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
    letter_occurrences = dict()
    for word in guess_words:
        letters_used = ""
        for letter in word:
            if letter not in letters_used:
                letter_occurrences[letter] = letter_occurrences.get(letter,0) + 1
                letters_used = letters_used + letter
    return letter_occurrences

def findBestGuess(poss_guess_words):
    """Given a list of possible guesses, choose the one that if chosen maximizes eliminations."""
    letter_occurrences = findCommonLetters(poss_guess_words)
    word_ratings = dict()
    guess_space_size = len(poss_guess_words)
    for guess_word in poss_guess_words:
        letters_used = ""
        for letter in guess_word:
            if letter not in letters_used:
                word_ratings[guess_word] = word_ratings.get(guess_word,float(0)) + \
                    rateGuessLetter(letter_occurrences[letter],guess_space_size)
                letters_used += letter
    best_guess_word = max(word_ratings, key=word_ratings.get)
    return best_guess_word

def trimPossGuesses(board_state, curr_guess_set):
    """Given a board, exclude the guesses that can no longer be the secret."""
    if len(board_state) == 0:
        return curr_guess_set
    new_guess_set = copy.deepcopy(curr_guess_set)
    for word in curr_guess_set:
        for letter_pos in range(len(word)):
            letter = word[letter_pos]
            if str(letter_pos) not in board_state.get(letter,set()):
                new_guess_set.remove(word)
                break
    return new_guess_set

def executeTurn(board_state, poss_guesses, secret, vPrint):
    """Make a guess and populate the board with it."""
    vPrint()
    new_poss_guesses = trimPossGuesses(board_state, poss_guesses)
    vPrint("in executeTurn, trimPossGuesses size", len(new_poss_guesses))
    best_guess = findBestGuess(new_poss_guesses)
    if best_guess == "2" or len(best_guess)<5 or len(new_poss_guesses)<1:
        # Serious error occurred if we pared all possibilities without finding the word
        print("in executeTurn, did not find a best guess with ---\nsecret:",secret,"\nand board state:\n",board_state,"\nand raw poss guesses:\n",poss_guesses,"\nand trimmed poss guesses:\n",new_poss_guesses)
        return True, board_state, new_poss_guesses
    vPrint("guessed",best_guess)
    new_board_state = processNewInfo(board_state, best_guess, secret)
    if(best_guess == secret):
        vPrint()
        return True, new_board_state, new_poss_guesses
    return False, new_board_state, new_poss_guesses

def solveGivenSecret(given_secret, verbose):
    """Auto-solve through all turns for a given secret."""
    verbosePrint = print if verbose else lambda *args, **kwargs: None
    f = open("secret.txt", "r")
    secrets_set = set(f.read().splitlines())
    print("len secrets_set:",len(secrets_set))
    if given_secret not in secrets_set:
        print("That isn't a possible secret")
    f = open("guess.txt", "r")
    guesses = set(f.read().splitlines())
    state_init_values = {'0','1','2','3','4'}
    state = {key: set(state_init_values) for key in list(string.ascii_lowercase)}
    turns_taken = 0
    while True:
        turns_taken += 1
        done, state, guesses  = executeTurn(state, guesses, given_secret, verbosePrint)
        if done:
            break
    return turns_taken

def avgAllSecrets():
    """Run solver on every possible secret, print avg time taken thru all."""
    f = open("secret.txt", "r")
    secrets_list = list(f.read().splitlines())
    secrets_solve_time = list()
    start_time = time.time()
    for secret in secrets_list:
        secrets_solve_time.append(solveGivenSecret(secret, verbose=False))
    end_time = time.time()
    print("max turns taken:",max(secrets_solve_time),"for",secrets_list[secrets_solve_time.index(max(secrets_solve_time))])
    print("min turns taken:",min(secrets_solve_time),"for",secrets_list[secrets_solve_time.index(min(secrets_solve_time))])
    print("avg turns taken:",sum(secrets_solve_time)/len(secrets_solve_time))
    print("avg seconds taken:",(end_time-start_time)/len(secrets_solve_time))

if __name__ == "__main__":
    try:
        solveGivenSecret(sys.argv[1], verbose=True)
    except IndexError:
        avgAllSecrets()
