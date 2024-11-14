import random

class ShipPlacer:
    def __init__(self, board_size):
        self.board_size = board_size
        self.num_ships = min(3, board_size - 1)

    def place_ships(self):
        ships = set()
        while len(ships) < self.num_ships:
            ship = (random.randint(0, self.board_size - 1), 
                   random.randint(0, self.board_size - 1))
            ships.add(ship)
        return ships