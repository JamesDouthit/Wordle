import sys
import string
import copy

def processNewInfo(guessable_map,new_guess,secret):
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

def findBestGuess(poss_guesses):
    guess_word = ""
    for guess in guess_word:
        pass
    return guess_word

def trimPossGuesses(board_state, curr_guess_set):
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
    new_poss_guesses = trimPossGuesses(board_state, poss_guesses)
    best_guess = findBestGuess(new_poss_guesses)
    print("guessed",best_guess)
    new_board_state = processNewInfo(board_state, best_guess, secret)
    if(best_guess == secret):
        return True, new_board_state, new_poss_guesses
    return False, new_board_state, new_poss_guesses

def solveGivenSecret(given_secret):
    # this is a set
    secrets_set = "./secret.txt"
    f = open("demofile.txt", "r")
    secrets_set = set(f.readlines())
    if given_secret not in secrets_set:
        print("That isn't a possible secret")
    # this is a set
    guesses = "./guess.txt"
    state = dict.fromkeys(list(string.ascii_lowercase))
    # state = dict()
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

{'a': {'Grey'}, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None, 'i': None, 'j': None, 'k': None, 'l': None, 'm': None, 'n': None, 'o': None, 'p': None, 'q': None, 'r': None, 's': None, 't': None, 'u': None, 'v': None, 'w': None, 'x': None, 'y': None, 'z': None}


letters
positions
colors
dynamic dict of letters with a list of positions mapping to colors

dict of positions with a dict of colors
dict of colors with dict of letters mapping to positions
^if letter in colors['black']

but most efficient is dict of letters to set of positions they can be in
{'a': {'0','1','2'}, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None, 'i': None, 'j': None, 'k': None, 'l': None, 'm': None, 'n': None, 'o': None, 'p': None, 'q': None, 'r': None, 's': None, 't': None, 'u': None, 'v': None, 'w': None, 'x': None, 'y': None, 'z': None}



old     {0,1,2,3,4}
new     1
result  {0,2,3,4}

old     {0,1,2,4}
new     1
result  {0,2,4}

old     {}
new     1
result  error

