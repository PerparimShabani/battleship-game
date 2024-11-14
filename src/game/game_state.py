class GameState:
    def __init__(self, board_size=5):
        self.board_size = board_size
        self.num_ships = min(3, self.board_size - 1)
        self.reset()
    
    def reset(self):
        self.player_board_state = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.computer_board_state = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.player_ships = set()
        self.computer_ships = set()
        self.player_guesses = set()
        self.computer_guesses = set()
        self.guess_history = []