from game import load_pokemon, game
from collections import defaultdict
from GuessingStrategy.guesser import shannon_entropy, knuth_mastermind, knuth_mastermind_avg

strategies = shannon_entropy, knuth_mastermind, knuth_mastermind_avg

def main():
    pokemon = load_pokemon('../Data/pokemon.csv')

    stats = defaultdict(list)

    for answer in pokemon:
        for strat in strategies:
            num_guesses, guesses, t = game(set(pokemon), answer, strat)
            stats[strat.__name__].append((str(num_guesses), f"{t:.4f}"))

    run_stats = zip(stats[shannon_entropy.__name__], stats[knuth_mastermind.__name__], stats[knuth_mastermind_avg.__name__])
    csv_string = "Shannon Guesses, Shannon Time, Knuth WC Guesses, Knuth WC Time, Knuth Avg Guesses, Knuth Avg Time\n"
    csv_string += "\n".join((",".join((",".join(entry) for entry in row))) for row in list(run_stats))

    with open("strategy_comparison.csv", "w") as f:
        f.write(csv_string)

if __name__ == "__main__":
    main()
