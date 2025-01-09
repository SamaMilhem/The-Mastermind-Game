import random
from collections import Counter

from solvers.solver import Solver, evaluate_guess


class QLearningSolver(Solver):
    def __init__(self,num_colors, code_length, epsilon, alpha, discount_factor,):
        super().__init__(num_colors, code_length)
        self.possible_states = None
        self.epsilon = epsilon
        self.alpha = alpha
        self.discount = discount_factor
        self.colors = num_colors
        self.code_length = code_length
        self.Q_values = Counter()  # Dictionary to store Q-values for state-action pairs
        self.reset_possible_states(self.colors**self.code_length)

    @staticmethod
    def _index_from_number(number, num_colors):
        """
        Convert a 4-digit guess to an index.
        Args:
            number (str): A 4-digit string representing the guess.
        Returns:
            int: The corresponding index.
        """
        return int(number, base=num_colors)

    @staticmethod
    def _number_from_index(index, num_colors, code_length):
        """
        Convert an index to a list of digits representing the guess.

        Args:
            index (int): The index to convert.
            num_colors (int): The number of possible colors.
            code_length (int): The length of the code.

        Returns:
            list: The corresponding list of digits representing the guess.
        """
        digits = []
        while index > 0:
            digits.append(index % num_colors)
            index //= num_colors

        return [0] * (code_length - len(digits)) + list(reversed(digits))

    def reset_possible_states(self, max_guesses):
        """
        Reset the possible states (guesses) for the agent.
        This is used to start each episode with a full set of possible guesses.
        """
        self.possible_states = [self._number_from_index(idx, self.colors, self.code_length)
                                for idx in range(max_guesses)]

    def restrict_possible_states(self, guess, feedback):
        """
        Restrict the possible states based on the feedback from a guess.
        This method filters out states that would not produce the same feedback as the given guess.
        """
        self.possible_states = [state for state in self.possible_states if evaluate_guess(guess, state) == feedback]

    def select_move(self):
        """
        Select the next move using an epsilon-greedy strategy.
        The agent may either explore (choose a random action) or exploit (choose the best-known action).
        """
        best_move = self.get_best_action()
        return best_move if random.random() > self.epsilon else self.random_action()

    def get_best_action(self):
        """
        Select the best action based on the current Q-values.
        If multiple actions have the same Q-value, one is chosen randomly.
        """

        max_value = max(self.Q_values[tuple(state)] for state in self.possible_states)
        best_actions = [state for state in self.possible_states if self.Q_values[tuple(state)] == max_value]
        return random.choice(best_actions)
    def random_action(self):
        """
        Select a random action from the possible states.
        """
        return random.choice(self.possible_states)

    def update(self, state, reward):
        """
        Update the Q-values using the Q-learning update rule.
        """
        best_next_value = max(self.Q_values[tuple(next_state)] for next_state in self.possible_states)
        td_target = reward + self.discount * best_next_value
        self.Q_values[tuple(state)] += self.alpha * (td_target - self.Q_values[tuple(state)])

    def learn(self, state, feedback, reward):
        """
        Learn from the state taken and its feedback by updating the Q-values.
        """
        self.restrict_possible_states(state, feedback)
        self.update(state, reward)

    def reward(self, guess, secret_code):
        """
        Determine the reward for a guess.
        """
        return 1 if guess == secret_code else -1

    def train(self, n_episodes):
        """
            Train the Q-learning agent over multiple episodes.
        """

        for _ in range(n_episodes):
            print(_)
            secret = random.randint(0, self.colors**self.code_length - 1)  # Generate a random secret code
            self.reset_possible_states(self.colors**self.code_length)
            guess = self.random_action()  # Start with a random guess

            while guess != self._number_from_index(secret,self.num_colors,self.code_length):
                feedback = evaluate_guess(guess, self._number_from_index(secret, self.num_colors, self.code_length))
                reward = self.reward(guess, secret)
                self.learn(guess, feedback, reward)
                if reward == 1:  # Correct guess, end episode
                    break
                guess = self.select_move()  # Select the next guess

    def solve(self, secret_code, guesses_threshold=50):
        self.reset_possible_states( self.colors**self.code_length)
        guess = self.get_best_action()
        num_guesses = 1
        guesses = []

        while guess != secret_code and num_guesses < guesses_threshold:
            feedback = evaluate_guess(guess, secret_code)
            guesses.append((guess, feedback))
            self.restrict_possible_states(guess, feedback)
            guess = self.get_best_action()
            num_guesses += 1

        feedback = evaluate_guess(guess, secret_code)
        guesses.append((guess, feedback))
        return guesses

