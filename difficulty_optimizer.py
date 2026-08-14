import random
import numpy as np
import optuna
from optuna.trial import Trial
from Solver.guesser import Guesser
from Solver.scorer import Scorer
from Solver.scoring_component import ScoringComponent, score_entropy, score_guess_in_answers, score_guess_pop
from Solver.selector import Selector, select_optimal, select_uniformly, select_weighted, select_k
from Solver.solver import Solver
from Solver.state_updater import StateUpdater, optimal_updater
from game import load_pokemon, GameInstance
from game_state import GameState
from pokemon import Pokemon, Attribute

pokemon = set(load_pokemon("Data/pokemon.csv"))
pokemon_list = list(pokemon)

def suggest_selector(t: Trial) -> Selector:
    kind = t.suggest_categorical("selector_kind", ["optimal", "uniform", "weighted", "k"])
    if kind == "optimal":
        return select_optimal
    if kind == "uniform":
        return select_uniformly
    if kind == "weighted":
        return select_weighted
    if kind == "k":
        k = t.suggest_int("selector_k_value", 1, 200)
        base = t.suggest_categorical("k_selector_base", ["uniform", "weighted"])
        if base == "optimal":
            return select_k(select_optimal, k)
        if base == "uniform":
            return select_k(select_uniformly, k)
        if base == "weighted":
            return select_k(select_weighted, k)
    raise ValueError("Invalid Selector Kind chosen")

def suggest_updater(t: Trial) -> StateUpdater:
    kind = t.suggest_categorical("updater_kind", ["optimal"])
    if kind == "optimal":
        return optimal_updater
    raise ValueError("Invalid Updater Kind chosen")

def suggest_components(t: Trial) -> list[tuple[ScoringComponent, float]]:
    entropy_weight = t.suggest_float("entropy_weight", 0, 5)
    pop_weight = t.suggest_float("pop_weight", 0, 5)
    in_answer_weight = t.suggest_float("in_answer_weight", 0, 5)
    return [
        (score_entropy, entropy_weight),
        (score_guess_pop, pop_weight),
        (score_guess_in_answers, in_answer_weight),
    ]

def run_game(scoring_comps: list[tuple[ScoringComponent, float]], selector: Selector, updater: StateUpdater, pokemon: set[Pokemon], answer: Pokemon) -> int:
    solver = Solver(Guesser(selector, Scorer(scoring_comps)), updater, GameState(pokemon, pokemon, 0, [], set(a for a in Attribute)))
    game = GameInstance(answer, [solver])
    score = game.run_game().state.turn
    return score


def optimize_difficulty(target: int, variance_weight: float, repeats: int):
    def optimize(trial: Trial):
        selector = suggest_selector(trial)
        updater = suggest_updater(trial)
        comps = suggest_components(trial)
        answers = random.choices(pokemon_list, k=repeats)
        turns = []
        for a in answers:
            turns.append(run_game(comps, selector, updater, pokemon, a))
        mean, stdev = np.mean(turns), np.std(turns)
        return abs(mean - target) + variance_weight * stdev

    return optimize

def main():
    storage = "sqlite:///difficulty_study.db"
    study = optuna.create_study(study_name="Find Medium Difficulty", direction="minimize", storage=storage, load_if_exists=True)
    study.optimize(optimize_difficulty(10, .2, 50), n_trials=25)

if __name__ == "__main__":
    main()