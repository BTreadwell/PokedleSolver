from typing import Protocol

from game_state import GameState
from pokemon import Pokemon, QueryResult


class StateUpdater(Protocol):
    def __call__(self, guess: Pokemon, response: QueryResult, curr_state: GameState) -> GameState:
        pass

def optimal_updater(guess: Pokemon, response: QueryResult, curr_state: GameState) -> GameState:
    curr_state.history.append((guess, response))
    curr_state.guesses.remove(guess)
    curr_state.turn += 1
    curr_state.answers = set([a for a in curr_state.answers if a.compare(guess) == response])
    return curr_state