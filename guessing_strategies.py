from pokemon import Pokemon
from collections import defaultdict

def knuth_mastermind(guesses: set[Pokemon], answers: set[Pokemon]) -> Pokemon:
    if len(answers) == 1:
        return answers.pop()

    best_guess, best_score = None, float('inf')
    for guess in guesses:
        answer_classes = defaultdict(int)
        for answer in answers:
            answer_classes[answer.compare(guess)] += 1
        score = max(answer_classes.values())
        if score < best_score:
            best_guess, best_score = guess, score
        elif score == best_score and best_guess not in answers:
            best_guess, best_score = guess, score
    return best_guess
