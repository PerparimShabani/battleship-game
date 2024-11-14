from flask import Flask, request, render_template_string
from src.game import game
import os

app = Flask(__name__)


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

    player_board_html = game.get_player_board_html()
    computer_board_html = game.get_computer_board_html()
    guess_history_html = game.get_guess_history_html()
    
    return render_template_string(HTML_TEMPLATE, 
                                message=message, 
                                player_board_html=player_board_html,
                                computer_board_html=computer_board_html,
                                guess_history_html=guess_history_html,
                                max_index=game.state.board_size-1)

@app.route('/reset', methods=['POST'])
def reset_game():
    game.reset_game()
    return web_game()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)