from flask import Flask, render_template, request, jsonify
import random
from solvers_factory import SolverFactory  # Import the factory


app = Flask(__name__, static_folder='static')

# Global Variables to Track the Game State
current_game = {
    "secret_code": [],
    "feedback": [],
    "num_colors": 6,
    "code_length": 4
}

@app.route("/")
def menu():
    return render_template("menu.html")

from flask import request

@app.route("/manual_game")
def manual_game():
    num_colors = int(request.args.get("num_colors", 6))
    current_game["num_colors"] = num_colors
    return render_template("manual_game.html")


@app.route("/q_learning_agent")
def qlearning_game():
    num_colors = int(request.args.get("num_colors", 6))
    current_game["num_colors"] = num_colors
    return render_template("q_learning_agent.html")


@app.route("/genetic_agent")
def genetic_game():
    num_colors = int(request.args.get("num_colors", 6))
    current_game["num_colors"] = num_colors
    return render_template("genetic_agent.html")

@app.route('/start_game', methods=['POST'])
def start_game():
    global current_game

    data = request.json
    num_colors = data.get('num_colors', 6)
    code_length = data.get('code_length', 4)
    secret_code = data.get('secret_code', None)  # Check if a secret code is provided

    current_game["num_colors"] = num_colors
    current_game["code_length"] = code_length

    if secret_code:  # Use the provided secret code
        current_game["secret_code"] = secret_code
    else:  # Generate a random secret code
        current_game["secret_code"] = [random.randint(0, num_colors - 1) for _ in range(code_length)]

    current_game["feedback"] = []
    print("Secret Code:", current_game["secret_code"])

    return jsonify({
        "message": "Game started!",
        "secret_code": current_game["secret_code"],
        "num_colors": num_colors,
        "code_length": code_length
    })



@app.route("/make_guess", methods=["POST"])
def make_guess():
    data = request.json
    guess = data.get("guess", [])

    if len(guess) != len(current_game["secret_code"]):
        return jsonify({"error": "Invalid guess length."}), 400
    # Calculate feedback
    black_pins = sum(
        1 for i, peg in enumerate(guess) if peg == current_game["secret_code"][i]
    )
    white_pins = len(set(guess) & set(current_game["secret_code"])) - black_pins

    feedback = (black_pins, white_pins)

    if black_pins == len(current_game["secret_code"]):
        return jsonify({"message": "You win!", "feedback": feedback})

    return jsonify({"feedback": feedback})


@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    algorithm = data.get('algorithm')
    print(current_game["secret_code"])
    if algorithm == 'genetic':
        # Create Genetic Solver using the factory
        genetic_solver = SolverFactory.create_solver(
            "genetic",
            num_colors=current_game["num_colors"],  # Override num_colors with user input
            code_length=current_game["code_length"]
        )
        guesses = genetic_solver.solve(secret_code=current_game["secret_code"])
        print(guesses)
        return jsonify({
            "message": f"Solved using Genetic Algorithm in {len(guesses)} turns.",
            "guesses": [list(guess) for guess in guesses]
        })

    elif algorithm == 'q_learning':
        # Create Q-Learning Solver using the factory
        qlearning_solver = SolverFactory.create_solver(
            "q_learning",
            num_colors=current_game["num_colors"],  # Override num_colors with user input
            code_length=current_game["code_length"]
        )
        guesses = qlearning_solver.solve(secret_code=current_game["secret_code"])
        return jsonify({
            "message": f"Solved using Q-Learning in {len(guesses)} turns.",
            "guesses": guesses
        })

    return jsonify({"error": "Invalid algorithm choice."}), 400


if __name__ == "__main__":
    app.run(debug=True)
