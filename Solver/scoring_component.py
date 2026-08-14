from collections import defaultdict
from typing import Protocol
from pokemon import Pokemon
from math import log2
from game_state import GameState

class ScoringComponent(Protocol):
    """
    API for scoring components
    They accept a guess and a current game state
    They return a score, lower for a worse guess and higher for a better guess, as determined by the specific component.
    """
    def __call__(self, g: Pokemon, curr_state: GameState) -> float:
        pass

def global_scoring_comp(value_func):
    """
    Decorator for scoring components that use the curr_state to find an optimal answer based on how much information it gives.
    :param value_func: function for measuring optimality of a guess (ie: entropy, Knuth WC/Avg)
    :return: ScoringComponent
    """
    def scoring_comp(g: Pokemon, curr_state: GameState) -> float:
        answer_classes = defaultdict(int)
        for answer in curr_state.answers:
            answer_classes[answer.compare_limited(g, set(curr_state.visibility))] += 1
        score = value_func(answer_classes.values())
        return score
    return scoring_comp

@global_scoring_comp
def score_avg_size(values: list[int]) -> float:
    """
    Scores a guess based on the average size of the answer partitions
    :param values: size of answer partitions
    :return: float
    """
    total = sum(values)
    return total - sum(v * v for v in values) / total

@global_scoring_comp
def score_entropy(values: list[int]) -> float:
    """
    Score a guess based on its entropy
    :param values: size of answer partitions
    :return: float, entropy of values
    """
    return sum(val / len(values) * log2(len(values) / val) for val in values)

@global_scoring_comp
def score_elim_values(values: list[int]) -> float:
    """
    Score a guess based on the size of its largest answer partition
    :param values: size of answer partitions
    :return: float, n - max(values)
    """
    return sum(values) - max(values)

def score_guess_pop(g: Pokemon, curr_state: GameState) -> float:
    """
    Score a guess based on its popularity/how well known the pokemon is
    :param g: Pokemon
    :param curr_state: GameState
    :return: float
    """
    return g.popularity

def score_guess_in_answers(g: Pokemon, curr_state: GameState) -> float:
    """
    Score a guess based on whether it is possibly a valid answer given the current game state
    :param g: Pokemon
    :param curr_state: GameState
    :return: float
    """
    return 1.0 if g in curr_state.answers else 0.0