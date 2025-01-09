from solvers.genetic_solver import GeneticSolver
from solvers.q_learning_solver import QLearningSolver
from fitness_strategies.peg_match_fitness import PegMatchFitness
from config import GENETIC_DEFAULTS, QLEARNING_DEFAULTS


class SolverFactory:
    """Factory for creating solver instances with default constants."""

    @staticmethod
    def create_solver(solver_type, **kwargs):
        """
        Factory method to create solver instances with defaults from `config.py`.

        Args:
            solver_type (str): The type of solver ("genetic" or "q_learning").
            **kwargs: Override default parameters if provided.

        Returns:
            Solver: An instance of the requested solver type.
        """
        if solver_type == "genetic":
            # Merge defaults with any provided overrides
            params = {**GENETIC_DEFAULTS, **kwargs}
            return GeneticSolver(
                num_colors=params["num_colors"],
                code_length=params["code_length"],
                pop_size=params["pop_size"],
                max_generation=params["max_generations"],
                elite_ratio=params["elite_ratio"],
                permutation_prob=params["permutation_prob"],
                inversion_prob=params["inversion_prob"],
                mutation_prob=params["mutation_prob"],
                crossover_prob=params["crossover_prob"],
                fitness_calculator=params.get("fitness_calculator", PegMatchFitness())
            )

        elif solver_type == "q_learning":
            # Merge defaults with any provided overrides
            params = {**QLEARNING_DEFAULTS, **kwargs}
            return QLearningSolver(
                num_colors=params["num_colors"],
                code_length=params["code_length"],
                epsilon=params["epsilon"],
                alpha=params["alpha"],
                discount_factor=params["discount_factor"]
            )

        else:
            raise ValueError(f"Unknown solver type: {solver_type}")