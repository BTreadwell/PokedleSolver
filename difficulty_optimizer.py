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

pokemon = set(load_pokemon("Data/pokemon_core.csv"))
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
        if base == "uniform":
            return select_k(select_uniformly, k)
        if base == "weighted":
            return select_k(select_weighted, k)
    raise ValueError("Invalid Selector Kind chosen")

def suggest_visibility(t: Trial) -> set[Attribute]:
    visibility = t.suggest_int("visbility_bitmap", 1, 63)
    fields = set()
    field_possibilities = [Attribute.GEN, Attribute.T1, Attribute.T2, Attribute.STAGE, Attribute.EVO, Attribute.COLOR]
    i = 0
    while visibility > 0:
        if visibility & 1:
            fields.add(field_possibilities[i])
        visibility >>= 1
        i += 1
    return fields

def suggest_components(t: Trial) -> list[tuple[ScoringComponent, float]]:
    entropy_weight = t.suggest_float("entropy_weight", 0, 5)
    pop_weight = t.suggest_float("pop_weight", 0, 5)
    in_answer_weight = t.suggest_float("in_answer_weight", 0, 5)
    return [
        (score_entropy, entropy_weight),
        (score_guess_pop, pop_weight),
        (score_guess_in_answers, in_answer_weight),
    ]

def run_game(scoring_comps: list[tuple[ScoringComponent, float]], selector: Selector, updater: StateUpdater, pokemon: set[Pokemon], answer: Pokemon, state: GameState) -> int:
    solver = Solver(Guesser(selector, Scorer(scoring_comps)), updater, state)
    game = GameInstance(answer, [solver])
    score = game.run_game().state.turn
    return score


def optimize_difficulty(target: int, variance_weight: float, repeats: int):
    def optimize(trial: Trial):
        selector = suggest_selector(trial)
        state_fields = suggest_visibility(trial)
        comps = suggest_components(trial)
        updater = optimal_updater
        answers = random.choices(pokemon_list, k=repeats)
        turns = []
        for a in answers:
            state = GameState(pokemon, pokemon, 0, [], state_fields)
            turns.append(run_game(comps, selector, updater, pokemon, a, state))
        mean, stdev = np.mean(turns), np.std(turns)
        return abs(mean - target) + variance_weight * stdev

    return optimize

def main():
    storage = "sqlite:///difficulty_study.db"
    study = optuna.create_study(study_name="Find Medium Difficulty", direction="minimize", storage=storage, load_if_exists=True)
    study.optimize(optimize_difficulty(10, .2, 90), n_trials=100)

if __name__ == "__main__":
    main()