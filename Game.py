from collections import defaultdict
from Pokemon import Pokemon
import random

def load_pokemon(pokemon_path: str) -> list[Pokemon]:
    pokemon = []
    with open(pokemon_path, 'r') as f:
        for line in f:
            tmp = [int(x) for x in line.strip().split(',')]
            pokemon.append(Pokemon(tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6]))
    return pokemon

def get_best_guess(guesses, answers) -> Pokemon:
    best_guess, best_size = None, len(answers)

    for guess in guesses:
        max_leftover = 0

        for answer in answers:
            curr_leftover = 0
            result = answer.compare(guess)

            for option in answers:
                if option is answer:
                    continue
                if option.is_compatible(guess, result):
                    curr_leftover += 1

            if curr_leftover > max_leftover:
                max_leftover = curr_leftover

        if max_leftover < best_size:
            best_guess = guess
            best_size = max_leftover

    return best_guess



def main():
    possible_answers = load_pokemon('Data/pokemon.csv')[:500]

    true_answer = random.choice(possible_answers)
    print("true answer", true_answer)
    solved = False

    num_guesses = 0
    while not solved:
        guess = get_best_guess(possible_answers, possible_answers)
        num_guesses += 1
        print("guess number", num_guesses, "\t", guess)
        result = true_answer.compare(guess)
        print("query result\t", result)
        if result == true_answer.compare(true_answer):
            solved = True
        else:
            possible_answers.remove(guess)
            possible_answers = [x for x in possible_answers if x.is_compatible(guess, result)]

if __name__ == '__main__':
    main()
