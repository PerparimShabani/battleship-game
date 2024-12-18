import random

class Board:
    def __init__(self, game_state):
        self.state = game_state

    def make_player_guess(self, row, col):
        if not self._is_valid_guess(row, col):
            return "Invalid guess! Please enter coordinates within the grid.", False

        if (row, col) in self.state.player_guesses:
            return "You already guessed that!", False

        self.state.player_guesses.add((row, col))
        self.state.guess_history.append(f"Player guessed ({row + 1}, {col + 1})")

        if (row, col) in self.state.computer_ships:
            self.state.update_board(row, col, 'X', is_player_board=False)
            self.state.computer_ships.remove((row, col))
            if not self.state.computer_ships:
                self.state.game_over = True
                result = "Hit! Congratulations! You sank all the computer's ships!"
            else:
                result = "Hit! You found a computer ship!"
            self.state.guess_history.append(result)
            return result, True
        else:
            self.state.update_board(row, col, 'O', is_player_board=False)
            result = "Miss! No computer ship at this location."
            self.state.guess_history.append(result)
            return result, True

    def make_computer_guess(self):
        if self.state.game_over:
            return "Game is already over!"

        row, col = self._get_random_guess()
        self.state.computer_guesses.add((row, col))
        self.state.guess_history.append(f"Computer guessed ({row + 1}, {col + 1})")

        if (row, col) in self.state.player_ships:
            self.state.update_board(row, col, 'X', is_player_board=True)
            self.state.player_ships.remove((row, col))
            if not self.state.player_ships:
                self.state.game_over = True
                result = "The computer hit your ship and sank all your ships! Game Over!"
            else:
                result = f"The computer hit your ship at ({row + 1}, {col + 1})!"
            self.state.guess_history.append(result)
            return result
        else:
            self.state.update_board(row, col, 'O', is_player_board=True)
            result = f"The computer missed at ({row + 1}, {col + 1})."
            self.state.guess_history.append(result)
            return result

    def _is_valid_guess(self, row, col):
        return 0 <= row < self.state.board_size and 0 <= col < self.state.board_size

    def _get_random_guess(self):
        while True:
            row = random.randint(0, self.state.board_size - 1)
            col = random.randint(0, self.state.board_size - 1)
            if (row, col) not in self.state.computer_guesses and self._is_valid_guess(row, col):
                return row, col