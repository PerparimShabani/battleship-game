import random

class Battleship:
    def __init__(self, size=5):
        self.board_size = size
        self.board = self.create_board()
        self.ship_row, self.ship_col = self.place_ship()
        self.guesses = set()
        self.max_turns = 10

    def create_board(self):
        return [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]

    def place_ship(self):
        return random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)

    def print_board(self):
        print('  ' + ' '.join(str(i) for i in range(self.board_size)))
        for i, row in enumerate(self.board):
            print(f"{i} {' '.join(row)}")

    def make_guess(self, row, col):
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            return "Oops, that's not even in the ocean."
        
        if (row, col) in self.guesses:
            return "You guessed that one already."
        
        self.guesses.add((row, col))
        
        if row == self.ship_row and col == self.ship_col:
            self.board[row][col] = 'X'
            return "Congratulations! You sunk my battleship!"
        else:
            self.board[row][col] = 'O'
            return "You missed my battleship!"

def play_game():
    game = Battleship()
    print("Welcome to Battleship!")
    print("Try to sink the ship within 10 turns.")

    for turn in range(game.max_turns):
        print(f"\nTurn {turn + 1}")
        game.print_board()
        
        try:
            guess_row = int(input("Guess Row (0-4): "))
            guess_col = int(input("Guess Col (0-4): "))
        except ValueError:
            print("Please enter valid numbers.")
            continue

        result = game.make_guess(guess_row, guess_col)
        print(result)
        
        if "Congratulations" in result:
            break
        
        if turn == game.max_turns - 1:
            print(f"Game Over. The ship was at {game.ship_row}, {game.ship_col}.")

if __name__ == "__main__":
    play_game()