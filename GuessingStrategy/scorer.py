from dataclasses import dataclass
from GuessingStrategy.scoring_component import score_entropy, score_guess_in_answers, score_elim_values, score_avg_size, ScoringComponent
from pokemon import Pokemon
from game_state import GameState
from collections import defaultdict

@dataclass
class Scorer:
    components: list[tuple[ScoringComponent, float]]

    def __call__(self, guesses: set[Pokemon], curr_state: GameState) -> dict[Pokemon, float]:
        raw_scores = defaultdict(dict)
        for i, (component, _) in enumerate(self.components):
            raw_scores[i] = {g : component(g, curr_state) for g in guesses}

        normed_scores = {i : normalize(raw_scores[i]) for i in range(len(self.components))}

        weighted_scores = defaultdict(float)
        for g in guesses:
            weighted_scores[g] = sum(normed_scores[i][g] * weight for i, (_, weight) in enumerate(self.components))

        return weighted_scores

def normalize(scores : dict[Pokemon, float]) -> dict[Pokemon, float]:
    low, high = min(scores.values()), max(scores.values())
    span = high - low
    if span == 0:
        return {g: 0 for g in scores}
    return {g: (score - low) / span for g, score in scores.items()}

optimal_entropy_scorer = Scorer([(score_entropy, 1.0)])
optimal_knuth_wc_scorer = Scorer([(score_elim_values, 1.0)])
optimal_knuth_avg_scorer = Scorer([(score_avg_size, 1.0)])