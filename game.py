import time
from dataclasses import dataclass
from typing import Callable
from guessing_strategies import knuth_mastermind
from pokemon import Pokemon, Response
import random

@dataclass
class GameState:
    answers: set[Pokemon]
    guesses: set[Pokemon]
    turn: int
    history: list[tuple[Pokemon, Response]]


def load_pokemon(pokemon_path: str) -> list[Pokemon]:
    pokemon = []
    with open(pokemon_path, 'r') as f:
        for line in f:
            tmp = [int(x) for x in line.strip().split(',')]
            pokemon.append(Pokemon(tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6]))
    return pokemon

def game(answers: set[Pokemon], answer: Pokemon, guessing_function: Callable[[set[Pokemon], set[Pokemon]], Pokemon]) -> tuple[int, list[Pokemon], float]:
    past_guesses = []
    guesses = answers.copy()
    num_guesses = 0
    start_time = time.time()
    while True:
        guess = guessing_function(guesses, answers)
        num_guesses += 1
        result = answer.compare(guess)
        if result[0] == Response.MATCH:
            return num_guesses, past_guesses, time.time() - start_time
        answers = set([a for a in answers if a.is_compatible(guess, result)])
        guesses.remove(guess)
        past_guesses.append(guess)

def main():
    answers = load_pokemon('Data/pokemon.csv')
    true_answer = random.choice(answers)
    num_guesses, guesses, t = game(set(answers), true_answer, knuth_mastermind)

    print("true answer", true_answer)
    print(f"Solved in {t} seconds using {num_guesses} guesses")
    # print(f"Guesses were: {",".join(map(str, guesses + [true_answer]))}")

if __name__ == '__main__':
    main()
