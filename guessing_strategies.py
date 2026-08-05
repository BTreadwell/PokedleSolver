from typing import Callable
import random
from pokemon import Pokemon
from collections import defaultdict
from math import log2

###########################################
# function for overall strategy
# (optional) sample guesses and/or answers
# score each guess against answers
# return guess with the best score
###########################################
def get_next_guess(guesses: set[Pokemon], answers: set[Pokemon], score_function: Callable[[list[int]], float],
                   sample_strategy: Callable[[set[Pokemon], set[Pokemon]], tuple[set[Pokemon], set[Pokemon]]] | None = None) -> Pokemon:
    if len(answers) == 1:
        return answers.pop()

    if sample_strategy is not None:
        guesses, answers = sample_strategy(guesses, answers)

    best_guess, best_score = None, float('inf')
    for guess in guesses:
        answer_classes = defaultdict(int)
        for answer in answers:
            answer_classes[answer.compare(guess)] += 1
        score = score_function(answer_classes.values())

        if score < best_score:
            best_guess, best_score = guess, score
        elif score == best_score and best_guess not in answers and guess in answers:
            best_guess, best_score = guess, score

    return best_guess

#######################
### Score Functions ###
#######################

# average score function
def avg(values: list[int]) -> float:
        return sum(values) / len(values)

# (inverse) entropy score function
def inv_entropy(values: list[int]) -> float:
    return sum(val / len(values) * log2(val / len(values)) for val in values)

##################################################################
### specific guessing strategies for convenience (no sampling) ###
##################################################################

# Knuth mastermind algorithm - find the guess that minimizes the size of remaining answers in the worst case (ie: minimax)
def knuth_mastermind(guesses: set[Pokemon], answers: set[Pokemon]) -> Pokemon:
    return get_next_guess(guesses, answers, max)

# Knuth mastermind algorithm modification - find the guess that minimizes the expected size of remaining answers
def knuth_mastermind_avg(guesses: set[Pokemon], answers: set[Pokemon]) -> Pokemon:
    return get_next_guess(guesses, answers, avg)

# Entropy approach - find the guess that maximizes entropy (minimizes inv entropy)
def shannon_entropy(guesses: set[Pokemon], answers: set[Pokemon]) -> Pokemon:
    return get_next_guess(guesses, answers, inv_entropy)

###########################
### Sampling strategies ###
###########################

def _sample_answers(sample_prop: float) -> Callable[[set[Pokemon], set[Pokemon]], tuple[set[Pokemon], set[Pokemon]]]:
    def sample_answers(guesses: set, answers: set) -> tuple[set, set]:
        return guesses, set(random.sample(list(answers), k=int(len(answers) * sample_prop)))
    return sample_answers

def _sample_guesses(sample_prop: float) -> Callable[[set[Pokemon], set[Pokemon]], tuple[set[Pokemon], set[Pokemon]]]:
    def sample_answers(guesses: set, answers: set) -> tuple[set, set]:
        return set(random.sample(list(guesses), k=int(len(guesses) * sample_prop))), answers
    return sample_answers

def _sample_both(sample_prop: float) -> Callable[[set[Pokemon], set[Pokemon]], tuple[set[Pokemon], set[Pokemon]]]:
    def sample_answers(guesses: set, answers: set) -> tuple[set, set]:
        return set(random.sample(list(guesses), k=int(len(guesses) * sample_prop))), set(random.sample(list(answers), k=int(len(answers) * sample_prop)))
    return sample_answers