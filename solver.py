import sys
import string
import copy
import time
import statistics

"""
rating func 1-(x^2)
max turns taken: 11 for eight
min turns taken: 2 for alien
avg turns taken: 5.193088552915767
avg seconds taken: 0.08743505786871035

rating func 1-(2*x^2)
max turns taken: 12 for hitch
min turns taken: 2 for apron
avg turns taken: 5.210799136069115
avg seconds taken: 0.09048486394449651

rating func 1-abs(x)
max turns taken: 12 for hitch
min turns taken: 1 for arose
avg turns taken: 5.110151187904967
avg seconds taken: 0.08604087953176148

rating func 1-((2x)^2)
max turns taken: 12 for hitch
min turns taken: 1 for arose
avg turns taken: 5.123110151187905
avg seconds taken: 0.09581264532925501
EASY MODE


rating func prandom
max turns taken: 11 for voter
min turns taken: 2 for broad
avg turns taken: 5.992656587473002
avg seconds taken: 0.07688286824566241
"""

# def hardCoded():
#     """For debug"""
#     # f = open("secret.txt", "r")
#     # secrets_set = set(f.read().splitlines())
#     f = open("guess.txt", "r")
#     guessable_set = set(f.read().splitlines())
#     my_sec_spc = {'swizz', 'stilt', 'stilb', 'spilt', 'still', 'blist', 'spill', 'blimp', 'slipt', 'swill'}
#     my_bg = findBestGuess(my_sec_spc,guessable_set)
#     print(my_sec_spc)

def determineTrueLetterCount()

def letterCorrectlyPlaced(checking_letter,checking_letter_position,checking_secret):
    """Checks if a letter is in the right place."""
    if not checking_letter in checking_secret:
        return False
    for secret_letter_position in range(len(checking_secret)):
        if checking_letter == checking_secret[secret_letter_position] and checking_letter_position == secret_letter_position:
            return True
    return False

def processNewGuess(guessable_map, true_letter_counts, new_guess, secret):
    """Populate the board with a new guess."""
    new_board_state = copy.deepcopy(guessable_map)
    new_true_letter_counts = copy.deepcopy(true_letter_counts)
    # keep track so we dont double count letters
    guess_letter_count_left = dict()
    for letter in new_guess:
        guess_letter_count_left[letter] = guess_letter_count_left.get(letter,0)+1
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
            guess_letter_count_left[letter] = guess_letter_count_left.get(letter,0)-1
        # letter in secret, but wrong place
        elif guess_letter_count_left[letter]>0:
            new_board_state[letter].discard(str(letter_pos))
            # account for the letter
            guess_letter_count_left[letter] = guess_letter_count_left.get(letter,0)-1
        # letter in secret but already accounted for
        elif guess_letter_count_left.get(letter,99)<=0:
            # now true number of this letter in the word is known
            new_board_state[letter].discard(str(letter_pos))
            new_true_letter_counts[letter] = ('=',secret.count(letter))
    return new_board_state, new_true_letter_counts

def rateGuessLetter(occurrences, space_size):
    """Rate a letter based on how close it comes to dividing the space in 2."""
    # raw_fraction = occurrences/space_size
    raw_fraction = 2*(0.5 - (occurrences/space_size))
    return 1 - abs(raw_fraction)
    # 1/1 -> 0
    # actual: 1-abs(0.5-1) = 0.5
    # 0/1 -> 0
    # actual: 1-abs(0.5-0) = 0.5
    # 0.5/1 -> 1
    # actual: 1-abs(0.5-0.5) = 1

def findLettersOccurrences(secret_space):
    """Count number of times letters occur in given guess words."""
    letter_occurrences = dict()
    for word in secret_space:
        letters_used = ""
        for letter in word:
            if letter not in letters_used:
                letter_occurrences[letter] = letter_occurrences.get(letter,0) + 1
                letters_used = letters_used + letter
    return letter_occurrences

def findBestGuess(secret_space, guess_space):
    """Given a list of possible guesses, choose the one that if chosen maximizes eliminations."""
    if len(secret_space)<=2:
        return list(secret_space)[0]
    secret_space_letter_occurrences = findLettersOccurrences(secret_space)
    guess_ratings = dict()
    secret_space_size = len(secret_space)
    for guess_word in guess_space:
        letters_used = ""
        # 
        # letter_ratings = []
        # letter_prevs = []
        # 
        for letter in guess_word:
            if letter not in letters_used:
                guess_ratings[guess_word] = guess_ratings.get(guess_word,float(0)) + \
                    rateGuessLetter(secret_space_letter_occurrences.get(letter, 0),secret_space_size)
                # 
                # letter_ratings.append(rateGuessLetter(secret_space_letter_occurrences.get(letter, 0),secret_space_size))
                # letter_prevs.append(secret_space_letter_occurrences.get(letter, 0))
                # 
                letters_used += letter
        # print("in findBestGuess,",len(secret_space),"word",guess_word,"rated",guess_ratings[guess_word])
        # print("from letters",list(guess_word),"rated",letter_ratings)
        # print("due to prevalences",letter_prevs)
    best_guess_word = max(guess_ratings, key=guess_ratings.get)
    return best_guess_word

def trimPossSecrets(board_state, known_letter_counts, curr_guess_set):
    """Given a board, exclude the guesses that can no longer be the secret."""
    if len(board_state) == 0:
        return curr_guess_set
    new_guess_set = copy.deepcopy(curr_guess_set)
    for word in curr_guess_set:
        word_letter_counts = dict()
        for curr_letter in word:
            word_letter_counts[curr_letter] = word_letter_counts.get(curr_letter,0)+1
        for letter_pos in range(len(word)):
            letter = word[letter_pos]
            if str(letter_pos) not in board_state.get(letter,set()):
                new_guess_set.remove(word)
                break
    return new_guess_set

def executeTurn(board_state, known_letter_counts, secret_space, secret, guess_space, vPrint):
    """Make a guess and populate the board with it."""
    vPrint()
    pared_secret_space = trimPossSecrets(board_state, known_letter_counts, secret_space)
    vPrint("in executeTurn, trimPossGuesses size", len(pared_secret_space))
    # 
    if len(pared_secret_space) < 11: vPrint("pared_secret_space", pared_secret_space)
    # 
    best_guess = findBestGuess(pared_secret_space, guess_space)
    if best_guess == "2" or len(best_guess)<5 or len(pared_secret_space)<1:
        # Serious error occurred if we pared all possibilities without finding the word
        print("in executeTurn, did not find a best guess with ---\nsecret:",secret,"\nand board state:\n",board_state,"\nand raw secret space:\n",secret_space,"\nand pared secret space:\n",pared_secret_space)
        return True, known_letter_counts, board_state, pared_secret_space
    vPrint("guessed",best_guess)
    new_board_state, new_known_letter_counts = processNewGuess(board_state, known_letter_counts, best_guess, secret)
    if(board_state == new_board_state and len(pared_secret_space)>1):
        print("in executeTurn, board not modified with ---\nsecret:",secret,"\nand board state:\n",board_state,"\nand NEW board state:\n",new_board_state,"\nand raw secret space:\n",secret_space,"\nand pared secret space:\n",pared_secret_space,"\nand guess:\n",best_guess)
        return True, known_letter_counts, board_state, pared_secret_space
    if((board_state == new_board_state) and best_guess != secret):
        print("in executeTurn, best_guess != secret with ---\nsecret:",secret,"\nand board state:\n",board_state,"\nand NEW board state:\n",new_board_state,"\nand raw secret space:\n",secret_space,"\nand pared secret space:\n",pared_secret_space,"\nand guess:\n",best_guess)
        return True, known_letter_counts, board_state, pared_secret_space
    if(best_guess == secret):
        # We found the secret!
        vPrint()
        return True, new_board_state, new_known_letter_counts, pared_secret_space
    return False, new_board_state, new_known_letter_counts, pared_secret_space

def solveGivenSecret(given_secret, verbose):
    """Auto-solve through all turns for a given secret."""
    verbosePrint = print if verbose else lambda *args, **kwargs: None
    f = open("secret.txt", "r")
    secrets_set = set(f.read().splitlines())
    if given_secret not in secrets_set:
        print("That isn't a possible secret")
    f = open("guess.txt", "r")
    guessable_set = set(f.read().splitlines())
    state_init_values = {'0','1','2','3','4'}
    state = {key: set(state_init_values) for key in list(string.ascii_lowercase)}
    known_counts = dict()
    secret_space = copy.deepcopy(guessable_set)
    turns_taken = 0
    while True:
        turns_taken += 1
        done, state, known_counts, secret_space = executeTurn(state, known_counts, secret_space, given_secret, guessable_set, verbosePrint)
        if done:
            print(given_secret,"found in",turns_taken,"turns!\n")
            break
    return turns_taken

def avgAllSecrets():
    """Run solver on every possible secret, print avg time taken thru all."""
    f = open("secret.txt", "r")
    secrets_list = list(f.read().splitlines())
    secrets_solve_turns = list()
    start_time = time.time()
    for secret in secrets_list:
        secrets_solve_turns.append(solveGivenSecret(secret, verbose=False))
        # 
        # print(secret,end=' ')
    end_time = time.time()
    print("max turns taken:",max(secrets_solve_turns),"for",secrets_list[secrets_solve_turns.index(max(secrets_solve_turns))])
    print("min turns taken:",min(secrets_solve_turns),"for",secrets_list[secrets_solve_turns.index(min(secrets_solve_turns))])
    print("avg turns taken:",sum(secrets_solve_turns)/len(secrets_solve_turns))
    print("variance turns taken:",statistics.variance(secrets_solve_turns))
    print("avg seconds taken:",(end_time-start_time)/len(secrets_solve_turns))

def main():
    """Implement options and kick off correct request"""
    # options = set()
    # secret = ""
    # for arg in sys.argv[1:]:
    #     if arg[0] == "-" and arg[1] == "h":
    #         print("Usage:")
    #         print("python solver.py <secret>")
    #         print("Options:")
    #         print("-v: verbose")
    #         print("-a: solve all secrets")
    #         print("-i: input custom with format")
    #         print("-r: run hardcoded prebuilt")
    #         return
    #     elif arg[0] == "-" and arg[1] == "v":
    #         options.add('v')
    #     elif arg[0] == "-" and arg[1] == "a":
    #         options.add('a')
    #     elif arg[0] == "-" and arg[1] == "i":
    #         options.add('i')
    #     elif arg[0] == "-" and arg[1] == "r":
    #         options.add('r')
    #     elif len(arg) == 5 and secret == "":
    #         secret = arg
    #     else:
    #         print("Errors in one or more args:",arg)
    #         return
    # if len(options)>1:
    #     print("Cannot combine two options")
    #     return
    # elif len(options) == 0:
    #     solveGivenSecret(sys.argv[1], verbose=False)
    # elif 'v' in options:
    #     solveGivenSecret(secret, verbose=True)
    # elif 'a' in options:
    #     avgAllSecrets()
    # elif 'i' in options:
    #     interactive()
    # elif 'r' in options:
    #     hardCoded()
    # return
    try:
        solveGivenSecret(sys.argv[1], verbose=True)
    except IndexError:
        avgAllSecrets()
    return

if __name__ == "__main__":
    main()
