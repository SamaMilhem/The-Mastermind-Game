from abc import ABC, abstractmethod


def evaluate_guess(guess, secret):
    """
    Compares the AI's guess with the secret code.
    Returns the number of pegs that are correct in both color and position (black pins)
    and the number of pegs that are correct in color but wrong in position (white pins).

    Args:
        guess (list): The AI's guess for the secret code.
        secret (list): The actual secret code.

    Returns:
        tuple: (black pins, white pins)
    """
    assert len(guess) == len(secret)

    # Count black pins (correct color and position)
    black_pins = sum(g == s for g, s in zip(guess, secret))

    # Remove matched (black pin) positions for further processing
    unmatched_guess = [g for g, s in zip(guess, secret) if g != s]
    unmatched_secret = [s for g, s in zip(guess, secret) if g != s]

    # Count white pins (correct color, wrong position)
    white_pins = 0
    for code in unmatched_guess:
        if code in unmatched_secret:
            white_pins += 1
            unmatched_secret.remove(code)  # Remove matched element to prevent re-counting

    return black_pins, white_pins


class Solver(ABC):
    """
    Abstract Base Class for all solvers.
    """
    def __init__(self, num_colors, code_length):
        self.num_colors = num_colors
        self.code_length = code_length

    @abstractmethod
    def solve(self, secret_code):
        """
        Solve the Mastermind puzzle.
        :param secret_code: The code to be guessed.
        :return: A list [(guess, feedback),...]
        """
        pass

