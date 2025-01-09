import random
from fitness_strategies.fitness_strategy import FitnessStrategy
from fitness_strategies.peg_match_fitness import PegMatchFitness
from solvers.solver import Solver, evaluate_guess


class GeneticSolver(Solver):
    def __init__(self, num_colors, code_length, pop_size, max_generation,elite_ratio,permutation_prob,
                 inversion_prob,mutation_prob, crossover_prob,fitness_calculator: FitnessStrategy):
        super().__init__(num_colors, code_length)
        self.pop_size = pop_size
        self.max_generations = max_generation
        self.elite_ratio = elite_ratio
        self.permutation_prob = permutation_prob
        self.inversion_prob = inversion_prob
        self.mutation_prob = mutation_prob
        self.crossover_prob = crossover_prob
        self.fitness_strategy = fitness_calculator

    def solve(self, secret_code, init_guess=None, white_pegs_weight=0.5, black_pegs_weight=0.5, penalty_weight=0):

        total_turns = 0
        previous_guesses = []
        prev_guesses_only = []
        code = [random.choice([_ for _ in range(self.num_colors)]) for _ in range(self.code_length)] \
            if not init_guess else init_guess

        result = evaluate_guess(code, secret_code)
        previous_guesses.append((tuple(code), result))
        prev_guesses_only.append(tuple(code))

        while result != (self.code_length, 0):
            eligibles = self.evolve_population(previous_guesses, white_pegs_weight, black_pegs_weight, total_turns, penalty_weight)

            if not eligibles:
                code = [random.choice([_ for _ in range(self.num_colors)]) for _ in range(self.code_length)]
            else:
                code = random.choice(list(eligibles))

            while code in prev_guesses_only:
                if not eligibles:
                    code = [random.choice([_ for _ in range(self.num_colors)]) for _ in range(self.code_length)]
                else:
                    code = random.choice(list[eligibles])

            total_turns += 1
            result = evaluate_guess(code, secret_code)
            previous_guesses.append((tuple(code), result))
            prev_guesses_only.append(tuple(code))

            if result == (self.code_length, 0):
                break
        return previous_guesses
    def evolve_population(self,previous_guesses, white_pegs_weight, black_pegs_weight, turn,
                          penalty_weight):
        """
        Performs a genetic algorithm to evolve a population of possible codes towards the correct code.
        Returns:
            list: A list of eligible codes that could potentially be the correct code.
        """

        population = [[random.choice([_ for _ in range(self.num_colors)]) for _ in range(self.code_length)]
                      for _ in range(self.pop_size)]
        eligibles = set()
        for _ in range(self.max_generations):
            fitness_scores = [(self.fitness_strategy.calculate_fitness(ind, previous_guesses, white_pegs_weight, black_pegs_weight, turn,
                          self.code_length, penalty_weight),ind) for ind in population]
            fitness_scores.sort(key=lambda x: x[0])

            num_elite = int(self.elite_ratio * self.pop_size)
            elite = [ind for _, ind in fitness_scores[:num_elite]]

            new_population = elite.copy()
            while len(new_population) < self.pop_size:
                parents = random.sample(elite, 2)

                offspring1, offspring2 = self.crossover(parents[0], parents[1])
                offspring1 = self.mutate(self.permute(self.invert(offspring1)))
                offspring2 =  self.mutate(self.permute(self.invert(offspring2)))
                new_population.extend([offspring1, offspring2])

            population = new_population[:self.pop_size]
            for score, ind in fitness_scores:
                if score == 0:
                    eligibles.add(tuple(ind))

        return eligibles

    def crossover(self,code1, code2):
        """
        Performs one-point or two-point crossover between two codes.
        """
        if random.random() < 0.5:
            point = random.randint(1, len(code1) - 1)
            return code1[:point] + code2[point:], code2[:point] + code1[point:]
        else:
            point1, point2 = sorted(random.sample(range(1, len(code1)), 2))
            return (code1[:point1] + code2[point1:point2] + code1[point2:],
                    code2[:point1] + code1[point1:point2] + code2[point2:])


    def mutate(self,code):
        if random.random() < self.mutation_prob:
            i = random.randint(0, self.code_length - 1)
            code[i] = random.choice([_ for _ in range(self.num_colors)])
        return code


    def permute(self,code):
        if random.random() < self.permutation_prob:
            pos1, pos2 = random.sample(range(self.code_length), 2)
            code[pos1], code[pos2] = code[pos2], code[pos1]
        return code


    def invert(self,code):
        if random.random() < self.inversion_prob:
            pos1, pos2 = sorted(random.sample(range(self.code_length), 2))
            code[pos1:pos2 + 1] = reversed(code[pos1:pos2 + 1])
        return code

