import os
import random
from flask import Flask, request, render_template_string

app = Flask(__name__)

class Battleship:
    def __init__(self, board_size=5):
        self.board_size = board_size
        self.num_ships = min(3, self.board_size - 1)
        self.reset_game()

    def reset_game(self):
        self.player_board = self.create_board()
        self.computer_board = self.create_board()
        self.player_ships = self.place_ships()
        self.computer_ships = self.place_ships()
        self.player_guesses = set()
        self.computer_guesses = set()

    def create_board(self):
        return [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]

    def place_ships(self):
        ships = set()
        while len(ships) < self.num_ships:
            ship = (random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1))
            ships.add(ship)
        return ships

    def make_guess(self, row, col):
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            return "Invalid guess! Please enter coordinates within the grid."

        if (row, col) in self.player_guesses:
            return "You already guessed that!"

        self.player_guesses.add((row, col))

        if (row, col) in self.computer_ships:
            self.computer_board[row][col] = 'X'
            self.computer_ships.remove((row, col))
            if not self.computer_ships:
                return "Congratulations! You sank all the computer's ships!"
            return "Hit! You found a computer ship!"
        else:
            self.computer_board[row][col] = 'O'
            return "Miss! No computer ship at this location."

    def computer_turn(self):
        while True:
            row, col = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)
            if (row, col) not in self.computer_guesses:
                break

        self.computer_guesses.add((row, col))

        if (row, col) in self.player_ships:
            self.player_board[row][col] = 'X'
            self.player_ships.remove((row, col))
            if not self.player_ships:
                return "Game Over! The computer sank all your ships!"
            return f"The computer hit your ship at ({row}, {col})!"
        else:
            self.player_board[row][col] = 'O'
            return f"The computer missed at ({row}, {col})."

    def get_board_html(self, board, guesses):
        html = "<table>"
        for i, row in enumerate(board):
            html += "<tr>"
            for j, cell in enumerate(row):
                if (i, j) in guesses:
                    html += f"<td>{cell}</td>"
                else:
                    html += "<td> </td>"
            html += "</tr>"
        html += "</table>"
        return html

game = Battleship()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Battleship Game</title>
    <style>
        table { border-collapse: collapse; margin-bottom: 20px; }
        td { width: 30px; height: 30px; border: 1px solid black; text-align: center; }
        .board-container { display: flex; justify-content: space-around; }
    </style>
</head>
<body>
    <h1>Battleship Game</h1>
    <p>{{ message }}</p>
    <div class="board-container">
        <div>
            <h2>Your Board</h2>
            {{ player_board_html | safe }}
        </div>
        <div>
            <h2>Computer's Board</h2>
            {{ computer_board_html | safe }}
        </div>
    </div>
    <form method="post">
        Row: <input type="number" name="row" min="0" max="{{ max_index }}" required>
        Col: <input type="number" name="col" min="0" max="{{ max_index }}" required>
        <input type="submit" value="Guess">
    </form>
    <form method="post" action="/reset">
        <input type="submit" value="Reset Game">
    </form>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def web_game():
    message = "Welcome to Battleship! Make your guess."
    if request.method == 'POST':
        row = int(request.form['row'])
        col = int(request.form['col'])
        message = game.make_guess(row, col)
        if "Congratulations" not in message and "Game Over" not in message:
            computer_message = game.computer_turn()
            message += " " + computer_message

    player_board_html = game.get_board_html(game.player_board, game.computer_guesses)
    computer_board_html = game.get_board_html(game.computer_board, game.player_guesses)
    return render_template_string(HTML_TEMPLATE, message=message, player_board_html=player_board_html, 
                                  computer_board_html=computer_board_html, max_index=game.board_size-1)

@app.route('/reset', methods=['POST'])
def reset_game():
    game.reset_game()
    return web_game()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)