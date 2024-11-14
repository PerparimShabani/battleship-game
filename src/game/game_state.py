import copy

class GameState:
    def __init__(self, board_size=5):
        self.board_size = board_size
        self.num_ships = min(3, self.board_size - 1)
        self.reset()
    
    def reset(self):
        # Initialize empty boards with spaces
        self.player_board_state = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.computer_board_state = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.player_ships = set()
        self.computer_ships = set()
        self.player_guesses = set()
        self.computer_guesses = set()
        self.guess_history = []
        self.game_over = False
        
    def update_board(self, row, col, value, is_player_board=True):
        board = self.player_board_state if is_player_board else self.computer_board_state
        board[row][col] = value
        
    def get_board_state(self, is_player_board=True):
        board = self.player_board_state if is_player_board else self.computer_board_state
        return copy.deepcopy(board)