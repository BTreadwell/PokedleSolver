from dataclasses import dataclass
from Solver.scorer import Scorer, optimal_entropy_scorer, optimal_knuth_wc_scorer, optimal_knuth_avg_scorer
from Solver.selector import Selector, select_optimal
from game_state import GameState
from pokemon import Pokemon

@dataclass
class Guesser:
    selector: Selector
    scorer: Scorer

    def __call__(self, game_state: GameState) -> Pokemon:
        if len(game_state.answers) == 1:
            return game_state.answers.pop()
        scored_guesses = self.scorer(game_state.guesses, game_state)
        return self.selector(scored_guesses, game_state)

optimal_entropy_guesser = Guesser(select_optimal, optimal_entropy_scorer)
optimal_knuth_wc_guesser = Guesser(select_optimal, optimal_knuth_wc_scorer)
optimal_knuth_avg_guesser = Guesser(select_optimal, optimal_knuth_avg_scorer)
