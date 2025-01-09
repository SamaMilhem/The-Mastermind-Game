# Default Constants for Genetic Algorithm Solver
GENETIC_DEFAULTS = {
    "num_colors": 6,
    "code_length": 4,
    "pop_size": 150,
    "max_generations": 100,
    "elite_ratio": 0.4,
    "permutation_prob": 0.03,
    "inversion_prob": 0.02,
    "mutation_prob": 0.03,
    "crossover_prob": 0.5
}

# Default Constants for Q-Learning Solver
QLEARNING_DEFAULTS = {
    "num_colors": 6,
    "code_length": 4,
    "epsilon": 0.4,
    "alpha": 0.3,
    "discount_factor": 0.8
}
