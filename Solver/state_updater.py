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
    answers = set([a for a in curr_state.answers if a.compare(guess) == response])
    return GameState(guesses, answers, turn, history)

def type_only_updater(guess: Pokemon, response: QueryResult, curr_state: GameState) -> GameState:
    history = curr_state.history + [(guess, response)]
    turn = curr_state.turn + 1
    guesses = curr_state.guesses.difference({guess})
    answers = set([a for a in curr_state.answers if a.compare(guess)[2] == response[2] and a.compare(guess)[3] == response[3]])
    return GameState(guesses, answers, turn, history)