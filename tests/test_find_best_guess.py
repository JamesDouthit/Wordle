import os

import wordle_solver

import unittest

class FindBestGuessTestCase(unittest.TestCase):

    def test_success(self):
        testing_dir = os.path.dirname(__file__)
        test_secret_space = {'swizz', 'stilt', 'stilb', 'spilt', 'still', 'blist', 'spill', 'blimp', 'slipt', 'swill'}
        test_guess_space = {'swizz'}
        bg = wordle_solver.solver.findBestGuess(
            test_secret_space, test_guess_space
        )
        self.assertEqual(
            bg, ""
        )
