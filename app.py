from flask import Flask, request, render_template, redirect
from src.game import Battleship
import os

app = Flask(__name__, template_folder='templates')
game = Battleship()

@app.route('/', methods=['GET', 'POST'])
def web_game():
    message = "Welcome to Battleship! Make your guess (rows and columns are 1-5)."
    if request.method == 'POST':
        try:
            # Convert 1-based input to 0-based index
            row = int(request.form['row']) - 1
            col = int(request.form['col']) - 1
            message, valid_guess = game.make_guess(row, col)
            if valid_guess and "Congratulations" not in message and "Game Over" not in message:
                computer_message = game.computer_turn()
                message += " " + computer_message
        except ValueError:
            message = "Please enter valid numbers for row and column (1-5)."

    player_board_html = game.get_player_board_html()
    computer_board_html = game.get_computer_board_html()
    guess_history_html = game.get_guess_history_html()
    
    return render_template('index.html', 
                         message=message, 
                         player_board_html=player_board_html,
                         computer_board_html=computer_board_html,
                         guess_history_html=guess_history_html,
                         max_index=game.state.board_size)  # Changed from board_size-1 to board_size

@app.route('/reset', methods=['GET', 'POST'])
def reset_game():
    game.reset_game()
    return redirect('/')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)