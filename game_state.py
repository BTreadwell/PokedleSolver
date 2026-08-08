from pokemon import Pokemon, QueryResult
from dataclasses import dataclass

@dataclass
class GameState:
    answers: set[Pokemon]
    guesses: set[Pokemon]
    turn: int
    history: list[tuple[Pokemon, QueryResult]]