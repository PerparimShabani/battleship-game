import random 

def create_board(size):
    """Create a game board of the specified size"""
    return [[' ' for _ in range (size)] for _ in range(size)]

def print_board(board):
    """Print the game board."""
    print(' ' + ' '.join(str(i) for i in range(len(board))))
    for i, row in enumerate(board):
        print(f"{i} {' '.join(row)}")
        
def place_ship(board):
    """Randomly place a ship on the board."""
    size = len(board)
    ship_row = random.randint(0, size - 1)
    ship_col = random.randint(0, size - 1)
    return ship_row, ship_col

def play_game():
    """Main function to play the Battleship game."""
    board_size = 5 
    board = create_board(board_size)
    ship_row, ship_col = place_ship(board)
    
    for turn in range(5):
        print(f"\nTurn {turn + 1}")
        print_board(board)
        
        try:
            guess_row = int(input("Guess Row (0-4): "))
            guess_col = int(input("Guess Col (0-4): "))
        except ValueError:
            print("Invalid input! Please enter numbers only.")
            continue 
        
        
        if (guess_row < 0 or guess_row >= board_size) or (guess_col < 0 or guess_col >= board_size):
                print("Oops, that's not even in the ocean.")
                continue
            
        if guess_row == ship_row and guess_col == ship_col:
            print("Congratulations! You sunk my battleship!")
            return
        elif board[guess_row][guess_col] == 'X':
                print("You guessed that one already.")
        else:
            print("You missed my Battleship!")
            board[guess_row][guess_col] = 'X'
                
        if turn == 4: 
            print(f"Game Over. The ship was at {ship_row}, {ship_col}.")

if __name__ == "__main__":
    play_game()