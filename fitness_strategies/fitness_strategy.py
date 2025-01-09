from abc import ABC, abstractmethod

class FitnessStrategy(ABC):
    """
    Abstract class for defining a fitness calculation strategy.
    """
    @abstractmethod
    def calculate_fitness(self, candidate, previous_guesses, white_pegs_weight, black_pegs_weight, turn,
                          code_length, penalty_weight=0) -> float:
        """
        Calculate the fitness score for a given candidate solution.
        """

        pass

