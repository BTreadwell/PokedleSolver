from Solver.guesser import Guesser, optimal_entropy_guesser
from Solver.state_updater import StateUpdater, optimal_updater
from game_state import GameState, Evaluator
from pokemon import Pokemon


class Solver:
    def __init__(self, guesser: Guesser, updater: StateUpdater, start_state: GameState):
        self.guesser = guesser
        self.updater = updater
        self.state = start_state
        self.guesses_made = 0

    def get_guess(self, evaluator: Evaluator) -> Pokemon:
        self.guesses_made += 1
        guess = self.guesser(self.state)
        response = evaluator.evaluate(guess)
        self.state = self.updater(guess, response, self.state)
        return guess

def get_optimal_solver(state: GameState) -> Solver:
    return Solver(optimal_entropy_guesser, optimal_updater, state)
