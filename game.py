import time
from Solver.solver import get_optimal_solver, Solver
from game_state import GameState, Evaluator
from pokemon import Pokemon, Attribute
import random

class GameInstance:
    def __init__(self, answer: Pokemon, solvers: list[Solver]):
        self.answer = answer
        self.solvers = solvers
        self.solver_turn = 0
        self.evaluator = Evaluator(answer)
        self.solved = False

    def run_game(self) -> Solver:
        while not self.solved:
            curr_solver = self.solvers[self.solver_turn]
            guess = curr_solver.get_guess(self.evaluator)
            if guess == self.answer:
                self.solved = True
                return curr_solver
            self.solver_turn = (self.solver_turn + 1) % len(self.solvers)


def load_pokemon(pokemon_path: str) -> list[Pokemon]:
    pokemon = []
    with open(pokemon_path, 'r') as f:
        for line in f:
            data = line.strip().split(',')
            pokemon.append(Pokemon(int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4]), bool(int(data[5])), int(data[6]), float(data[7])))
    return pokemon

def timed_game(game_set: set[Pokemon], answer: Pokemon) -> tuple[GameState, float]:
    game_state = GameState(game_set, game_set, 0, [], set(a for a in Attribute))
    solver = get_optimal_solver(game_state)
    game = GameInstance(answer, [solver])
    start_time = time.time()
    solver = game.run_game()
    return solver.state, time.time() - start_time

def main():
    answers = load_pokemon('Data/pokemon_w_pop.csv')
    true_answer = random.choice(answers)
    game_state, t = timed_game(set(answers), true_answer)

    print("true answer", true_answer)
    print(f"Solved in {t} seconds using {game_state.turn} guesses")
    print(f"Guesses were: {",".join([str(x[0]) for x in game_state.history])}")

if __name__ == '__main__':
    main()
