from guessing_strategies import knuth_mastermind
from pokemon import Pokemon
import random

def load_pokemon(pokemon_path: str) -> list[Pokemon]:
    pokemon = []
    with open(pokemon_path, 'r') as f:
        for line in f:
            tmp = [int(x) for x in line.strip().split(',')]
            pokemon.append(Pokemon(tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6]))
    return pokemon

def main():
    possible_answers = load_pokemon('Data/pokemon.csv')

    true_answer = random.choice(possible_answers)
    print("true answer", true_answer)
    solved = False

    num_guesses = 0
    while not solved:
        guess = knuth_mastermind(set(possible_answers), set(possible_answers))
        num_guesses += 1
        print("guess number", num_guesses, "\t", guess)
        result = true_answer.compare(guess)
        if result == true_answer.compare(true_answer):
            solved = True
        else:
            possible_answers.remove(guess)
            possible_answers = [x for x in possible_answers if x.is_compatible(guess, result)]

if __name__ == '__main__':
    main()
