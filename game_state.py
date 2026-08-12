from pokemon import Pokemon, QueryResult
from dataclasses import dataclass

@dataclass
class GameState:
    answers: set[Pokemon]
    guesses: set[Pokemon]
    turn: int
    history: list[tuple[Pokemon, QueryResult]]

class Evaluator:
    def __init__(self, answer: Pokemon):
        self.answer = answer

    def evaluate(self, guess: Pokemon) -> QueryResult:
        return self.answer.compare(guess)