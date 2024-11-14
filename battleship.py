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
        self.guess_history = []  # Add guess history list

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
            return "Invalid guess! Please enter coordinates within the grid.", False

        if (row, col) in self.player_guesses:
            return "You already guessed that!", False

        self.player_guesses.add((row, col))
        self.guess_history.append(f"Player guessed ({row}, {col})")

        if (row, col) in self.computer_ships:
            self.computer_board[row][col] = 'X'
            self.computer_ships.remove((row, col))
            result = "Congratulations! You sank all the computer's ships!" if not self.computer_ships else "Hit! You found a computer ship!"
            self.guess_history.append(result)
            return result, True
        else:
            self.computer_board[row][col] = 'O'
            result = "Miss! No computer ship at this location."
            self.guess_history.append(result)
            return result, True

    def computer_turn(self):
        while True:
            row, col = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)
            if (row, col) not in self.computer_guesses:
                break

        self.computer_guesses.add((row, col))
        self.guess_history.append(f"Computer guessed ({row}, {col})")

        if (row, col) in self.player_ships:
            self.player_board[row][col] = 'X'
            self.player_ships.remove((row, col))
            result = "Game Over! The computer sank all your ships!" if not self.player_ships else f"The computer hit your ship at ({row}, {col})!"
            self.guess_history.append(result)
            return result
        else:
            self.player_board[row][col] = 'O'
            result = f"The computer missed at ({row}, {col})."
            self.guess_history.append(result)
            return result

    def get_board_html(self, board, guesses):
        html = "<table>"
        for i, row in enumerate(board):
            html += "<tr>"
            for j, cell in enumerate(row):
                cell_class = ""
                if (i, j) in guesses:
                    cell_class = "hit" if cell == 'X' else "miss"
                html += f'<td class="{cell_class}">{cell if (i, j) in guesses else " "}</td>'
            html += "</tr>"
        html += "</table>"
        return html

    def get_guess_history_html(self):
        html = "<ul>"
        for move in self.guess_history:
            html += f"<li>{move}</li>"
        html += "</ul>"
        return html

game = Battleship()

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
        td { 
            width: 30px; 
            height: 30px; 
            border: 1px solid black; 
            text-align: center; 
        }
        .board-container { display: flex; justify-content: space-around; }
        .hit { background-color: #ef5350; color: white; }
        .miss { background-color: #90caf9; color: white; }
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
    <div class="guess-history">
        <h3>Game History</h3>
        {{ guess_history_html | safe }}
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
        try:
            row = int(request.form['row'])
            col = int(request.form['col'])
            message, valid_guess = game.make_guess(row, col)
            if valid_guess and "Congratulations" not in message and "Game Over" not in message:
                computer_message = game.computer_turn()
                message += " " + computer_message
        except ValueError:
            message = "Please enter valid numbers for row and column."

    player_board_html = game.get_board_html(game.player_board, game.computer_guesses)
    computer_board_html = game.get_board_html(game.computer_board, game.player_guesses)
    guess_history_html = game.get_guess_history_html()
    
    return render_template_string(HTML_TEMPLATE, 
                                message=message, 
                                player_board_html=player_board_html,
                                computer_board_html=computer_board_html,
                                guess_history_html=guess_history_html,
                                max_index=game.board_size-1)

@app.route('/reset', methods=['POST'])
def reset_game():
    game.reset_game()
    return web_game()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)