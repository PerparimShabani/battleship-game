from flask import Flask, render_template, request
from battleship import Battleship

app = Flask(__name__)
game = Battleship()

@app.route('/', methods=['GET', 'POST'])
def web_game():
    message = "Welcome to Battleship! Make your guess."
    if request.method == 'POST':
        try:
            row = int(request.form['row'])
            col = int(request.form['col'])
            message = game.make_guess(row, col)
            if "Congratulations" not in message and "Game Over" not in message:
                computer_message = game.computer_turn()
                message += " " + computer_message
        except ValueError:
            message = "Please enter valid numbers for row and column."

    player_board_html = game.get_board_html(game.player_board, game.computer_guesses)
    computer_board_html = game.get_board_html(game.computer_board, game.player_guesses)
    guess_history_html = game.get_guess_history_html()
    
    return render_template('index.html',
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
    app.run(debug=True)