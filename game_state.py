from pokemon import Pokemon, QueryResult, Attribute
from dataclasses import dataclass

@dataclass
class GameState:
    answers: set[Pokemon]
    guesses: set[Pokemon]
    turn: int
    history: list[tuple[Pokemon, QueryResult]]
    visibility: set[Attribute]

class Evaluator:
    def __init__(self, answer: Pokemon):
        self.answer = answer

    def evaluate(self, guess: Pokemon) -> QueryResult:
        return self.answer.compare(guess)