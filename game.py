import time
from typing import Callable
from Solver.guesser import optimal_entropy_guesser
from Solver.solver import get_optimal_solver
from game_state import GameState
from pokemon import Pokemon, Response
import random

def load_pokemon(pokemon_path: str) -> list[Pokemon]:
    pokemon = []
    with open(pokemon_path, 'r') as f:
        for line in f:
            tmp = [int(x) for x in line.strip().split(',')]
            pokemon.append(Pokemon(tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6]))
    return pokemon

def timed_game(game_set: set[Pokemon], answer: Pokemon) -> tuple[GameState, float]:
    game_state = GameState(game_set, game_set, 0, [])
    solver = get_optimal_solver(game_state)
    start_time = time.time()
    while True:
        guess = solver.get_guess()
        result = answer.compare(guess)
        solver.update_state(guess, result)

        if result[0] == Response.MATCH:
            return solver.state, time.time() - start_time

def main():
    answers = load_pokemon('Data/pokemon.csv')
    true_answer = random.choice(answers)
    game_state, t = timed_game(set(answers), true_answer)

    print("true answer", true_answer)
    print(f"Solved in {t} seconds using {game_state.turn} guesses")
    print(f"Guesses were: {",".join([str(x[0]) for x in game_state.history])}")

if __name__ == '__main__':
    main()
