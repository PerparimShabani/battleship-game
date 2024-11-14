from .game_state import GameState
from .board import Board
from .ship_placer import ShipPlacer
from .renderer import BoardRenderer

class Battleship:
    def __init__(self, board_size=5):
        self.state = GameState(board_size)
        self.board = Board(self.state)
        self.ship_placer = ShipPlacer(board_size)
        self.renderer = BoardRenderer()
        self.reset_game()

    def reset_game(self):
        self.state.reset()
        self.state.player_ships = self.ship_placer.place_ships()
        self.state.computer_ships = self.ship_placer.place_ships()

    def make_guess(self, row, col):
        return self.board.make_player_guess(row, col)

    def computer_turn(self):
        return self.board.make_computer_guess()

    def get_player_board_html(self):
        return self.renderer.get_board_html(self.state.player_board_state)

    def get_computer_board_html(self):
        return self.renderer.get_board_html(self.state.computer_board_state)

    def get_guess_history_html(self):
        return self.renderer.get_guess_history_html(self.state.guess_history)

game = Battleship()