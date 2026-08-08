from typing import Protocol
from dataclasses import dataclass
import random
from game_state import GameState
from pokemon import Pokemon

class SelectionMethod(Protocol):
    def __call__(self, scored_guesses: dict[Pokemon, float], curr_state: GameState) -> Pokemon:
        pass

def select_optimal(scored_guesses: dict[Pokemon, float], curr_state: GameState) -> Pokemon:
    max_score = max(scored_guesses.values())
    opt_guesses = set(g for (g, v) in scored_guesses.items() if v == max_score)
    try:
        return random.choice(list(opt_guesses.intersection(curr_state.answers)))
    except IndexError:
        return random.choice(list(opt_guesses))

def select_uniformly(scored_guesses: dict[Pokemon, float], curr_state: GameState) -> Pokemon:
    return random.choice(list(scored_guesses))

def select_weighted(scored_guesses: dict[Pokemon, float], curr_state: GameState) -> Pokemon:
    guesses, weights = zip(*[(k, v) for k, v in scored_guesses.items()])
    return random.choices(guesses, weights=weights)[0]

@dataclass
class Selector:
    selection_method: SelectionMethod

    def __call__(self, scored_guesses: dict[Pokemon, float], curr_state: GameState) -> Pokemon:
        return self.selection_method(scored_guesses, curr_state)

optimal_selector = Selector(select_optimal)
uniform_selector = Selector(select_uniformly)
weighted_selector = Selector(select_weighted)