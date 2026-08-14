from typing import Protocol

from game_state import GameState
from pokemon import Pokemon, QueryResult


class StateUpdater(Protocol):
    def __call__(self, guess: Pokemon, response: QueryResult, curr_state: GameState) -> GameState:
        pass

def optimal_updater(guess: Pokemon, response: QueryResult, curr_state: GameState) -> GameState:
    history = curr_state.history + [(guess, response)]
    turn = curr_state.turn + 1
    guesses = curr_state.guesses.difference({guess})
    answers = set([a for a in curr_state.answers if a.is_compatible(guess, response, list(curr_state.visibility))])
    visibility = set(f for f in curr_state.visibility)
    return GameState(guesses, answers, turn, history, visibility)

