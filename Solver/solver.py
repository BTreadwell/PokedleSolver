from Solver.guesser import Guesser, optimal_entropy_guesser
from Solver.state_updater import StateUpdater, optimal_updater
from game_state import GameState
from pokemon import Pokemon, QueryResult


class Solver:
    def __init__(self, guesser: Guesser, updater: StateUpdater, start_state: GameState):
        self.guesser = guesser
        self.updater = updater
        self.state = start_state
        self.guesses_made = 0

    def get_guess(self) -> Pokemon:
        self.guesses_made += 1
        return self.guesser(self.state)

    def update_state(self, guess: Pokemon, response: QueryResult):
        self.state = self.updater(guess, response, self.state)

def get_optimal_solver(state: GameState) -> Solver:
    return Solver(optimal_entropy_guesser, optimal_updater, state)
