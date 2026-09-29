from Solver.guesser import Guesser, optimal_entropy_guesser, player_guesser
from Solver.state_updater import StateUpdater, optimal_updater, player_updater
from game_state import GameState, Evaluator
from pokemon import Pokemon, QueryResult


class Solver:
    """
    Representation of a Pokedle Player.
    A Solver uses a Guesser, StateUpdater, and GameState to play pokedle.
    """
    def __init__(self, guesser: Guesser, updater: StateUpdater, start_state: GameState):
        """
        Parameters
        ----------
        guesser: Guesser
        updater: StateUpdater
        start_state: GameState
        """
        self.guesser = guesser
        self.updater = updater
        self.state = start_state
        self.guesses_made = 0

    def take_turn(self, evaluator: Evaluator) -> Pokemon:
        """
        Query the Solver for a guess and internally update the state
        Parameters
        ----------
        evaluator: Evaluator

        Returns
        -------
        Pokemon, the solvers guess based on its internal state
        """
        self.guesses_made += 1
        guess = self.guesser(self.state)
        response = evaluator.evaluate(guess)
        self.state = self.updater(guess, response, self.state)
        return guess

    def see_guess(self, guess: Pokemon, response: QueryResult) -> None:
        """
        Update the solvers state based on an observed guess/response pair.
        Parameters
        ----------
        guess: Pokemon
        response: QueryResult
        """
        self.state = self.updater(guess, response, self.state)

    def just_guess(self):
        """
        Query the Solver for a guess and DO NOT update the internal state.
        Returns
        -------
        Pokemon, the solvers guess based on its internal state
        """
        return self.guesser(self.state)

def get_optimal_solver(state: GameState) -> Solver:
    """
    Creates a solver that uses an optimal, entropy-based guesser with a complete state updater.
    Parameters
    ----------
    state: GameState, starting state for the solver

    Returns
    -------
    Solver
    """
    return Solver(optimal_entropy_guesser, optimal_updater, state)

def get_player_solver(state: GameState) -> Solver:
    """
    Creates a solver that allows for player-input guesses with a minimal state updater
    Parameters
    ----------
    state: GameState

    Returns
    -------
    Solver
    """
    return Solver(player_guesser, player_updater, state)