import time
from typing import Callable
from GuessingStrategy.guesser import optimal_entropy_guesser
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

def game(answers: set[Pokemon], answer: Pokemon, guessing_function: Callable[[set[Pokemon], set[Pokemon]], Pokemon]) -> tuple[GameState, float]:
    game_state = GameState(answers, answers, 1, [])
    start_time = time.time()
    while True:
        guess = guessing_function(game_state)
        result = answer.compare(guess)
        if result[0] == Response.MATCH:
            return game_state, time.time() - start_time
        game_state.answers = set([a for a in game_state.answers if a.is_compatible(guess, result)])
        game_state.guesses.remove(guess)
        game_state.history.append((guess, result))
        game_state.turn += 1

def main():
    answers = load_pokemon('Data/pokemon.csv')
    true_answer = random.choice(answers)
    game_state, t = game(set(answers), true_answer, optimal_entropy_guesser)

    print("true answer", true_answer)
    print(f"Solved in {t} seconds using {game_state.turn} guesses")
    # print(f"Guesses were: {",".join(map(str, guesses + [true_answer]))}")

if __name__ == '__main__':
    main()
