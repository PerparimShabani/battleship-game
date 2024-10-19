import os
import random
from flask import Flask, request, render_template_string

app = Flask(__name__)

class Battleship:
    def __init__(self, board_size=5):
        """
        Initialize the Battleship game.
        :param board_size: Size of the game board (5-10)
        """
        self.board_size = max(5, min(10, board_size))  # Ensure board size is between 5 and 10
        self.num_ships = min(3, self.board_size - 1)  # Adjust number of ships based on board size
        self.board = self.create_board()
        self.ships = self.place_ships()
        self.guesses = set()

    def create_board(self):
        """Create an empty game board."""
        return [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]

    def place_ships(self):
        """Randomly place ships on the board."""
        ships = set()
        while len(ships) < self.num_ships:
            ship = (random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1))
            ships.add(ship)
        return ships

    def is_valid_guess(self, row, col):
        """Check if the guess is within the board boundaries."""
        return 0 <= row < self.board_size and 0 <= col < self.board_size

    def make_guess(self, row, col):
        """
        Process a player's guess.
        :param row: Row of the guess
        :param col: Column of the guess
        :return: Result of the guess
        """
        if not self.is_valid_guess(row, col):
            return "Invalid guess! Please enter coordinates within the grid."

        if (row, col) in self.guesses:
            return "You already guessed that!"

        self.guesses.add((row, col))

        if (row, col) in self.ships:
            self.board[row][col] = 'X'
            self.ships.remove((row, col))
            if not self.ships:
                return "Congratulations! You sank all the ships!"
            return "Hit! You found a ship!"
        else:
            self.board[row][col] = 'O'
            return "Miss! No ship at this location."

    def get_board_html(self):
        """Generate HTML representation of the game board."""
        html = "<table>"
        for row in self.board:
            html += "<tr>"
            for cell in row:
                html += f"<td>{cell}</td>"
            html += "</tr>"
        html += "</table>"
        return html

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Battleship Game</title>
    <style>
        table { border-collapse: collapse; }
        td { width: 30px; height: 30px; border: 1px solid black; text-align: center; }
    </style>
</head>
<body>
    <h1>Battleship Game</h1>
    <p>{{ message }}</p>
    {{ board_html | safe }}
    <form method="post">
        Row: <input type="number" name="row" min="0" max="{{ max_index }}" required>
        Col: <input type="number" name="col" min="0" max="{{ max_index }}" required>
        <input type="submit" value="Guess">
    </form>
</body>
</html>
'''

game = Battleship()

@app.route('/', methods=['GET', 'POST'])
def web_game():
    message = "Welcome to Battleship! Make your guess."
    if request.method == 'POST':
        row = int(request.form['row'])
        col = int(request.form['col'])
        message = game.make_guess(row, col)
    
    board_html = game.get_board_html()
    return render_template_string(HTML_TEMPLATE, message=message, board_html=board_html, max_index=game.board_size-1)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)