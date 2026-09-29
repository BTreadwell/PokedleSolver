from typing import Protocol

from game_state import GameState
from pokemon import Pokemon, QueryResult


class StateUpdater(Protocol):
    """
    Protocol for updating GameState objects after observing a guess/response pair
    """
    def __call__(self, guess: Pokemon, response: QueryResult, curr_state: GameState) -> GameState:
        pass

def optimal_updater(guess: Pokemon, response: QueryResult, curr_state: GameState) -> GameState:
    """
    Optimal state updater that leverages all available information to eliminate impossible answers from consideration
    Parameters
    ----------
    guess: Pokemon
    response: QueryResult
    curr_state: GameState,

    Returns
    -------
    GameState
    """
    history = [_ for _ in curr_state.history] + [(guess, response)]
    turn = curr_state.turn + 1
    guesses = curr_state.guesses.difference({guess})
    answers = set([a for a in curr_state.answers if a.is_compatible(guess, response, list(curr_state.visibility))])
    visibility = set(f for f in curr_state.visibility)
    return GameState(answers, guesses, turn, history, visibility)

def player_updater(guess: Pokemon, response: QueryResult, curr_state: GameState) -> GameState:
    """
    Minimal updater for use in player-based solvers.
    Does not track possible answers or GameState.visiblitiy
    Parameters
    ----------
    guess: Pokemon
    response: QueryResult
    curr_state: GameState

    Returns
    -------
    GameState (empty/default values for answers and visibility)
    """
    history = curr_state.history + [(guess, response)]
    turn = curr_state.turn + 1
    guesses = curr_state.guesses.difference({guess})
    return GameState(set(), guesses, turn, history, set())