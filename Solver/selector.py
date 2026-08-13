from typing import Protocol
import random
from game_state import GameState
from pokemon import Pokemon

class Selector(Protocol):
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
    try:
        return random.choices(guesses, weights=weights)[0]
    except ValueError:
        return random.choice(list(scored_guesses))

def select_k(selector: Selector, k: int) -> Selector:
    def k_selector(scored_guesses: dict[Pokemon, float], curr_state: GameState):
        top_k = {g: v for (g, v) in sorted(list(scored_guesses.items()), key=lambda x : x[1], reverse=True)[:k]}
        return selector(top_k, curr_state)
    return k_selector
