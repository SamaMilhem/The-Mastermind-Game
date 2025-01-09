from fitness_strategies.fitness_strategy import FitnessStrategy
from solvers.solver import evaluate_guess


class PegMatchFitness(FitnessStrategy):
    """
    Fitness is calculated based on the number of black and white pegs.
    """

    def calculate_fitness(self, candidate, previous_guesses, white_pegs_weight, black_pegs_weight, turn,
                          code_length, penalty_weight=0 ) -> float:

        def get_difference(trial, prev_guess):
            guess_result = prev_guess[1]
            guess_code = prev_guess[0]
            trial_result = evaluate_guess(trial, guess_code)
            dif = [abs(trial_result[i] - guess_result[i]) for i in range(2)]
            return tuple(dif)

        differences = [get_difference(candidate, prev_guess) for prev_guess in previous_guesses]
        sum_black_pin_differences = sum(dif[0] for dif in differences)
        sum_white_pin_differences = sum(dif[1] for dif in differences)

        fitness_score = (black_pegs_weight * sum_black_pin_differences + white_pegs_weight * sum_white_pin_differences +
                         penalty_weight * code_length * (turn-1))
        return fitness_score
