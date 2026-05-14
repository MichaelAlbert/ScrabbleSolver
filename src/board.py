# Represents a 15x15 standard Scrabbble board.

TRIPLE_WORD = [
    (0,0),(0,7),(0,14),
    (7,0),(7,14),
    (14,0),(14,7),(14,14)
]

DOUBLE_WORD = [
    (1,1),(2,2),(3,3),(4,4),
    (7,7),
    (10,10),(11,11),(12,12),(13,13),
    (1,13),(2,12),(3,11),(4,10),
    (10,4),(11,3),(12,2),(13,1)
]

TRIPLE_LETTER = [
    (1,5),(1,9),
    (5,1),(5,5),(5,9),(5,13),
    (9,1),(9,5),(9,9),(9,13),
    (13,5),(13,9)
]

DOUBLE_LETTER = [
    (0,3),(0,11),
    (2,6),(2,8),
    (3,0),(3,7),(3,14),
    (6,2),(6,6),(6,8),(6,12),
    (7,3),(7,11),
    (8,2),(8,6),(8,8),(8,12),
    (11,0),(11,7),(11,14),
    (12,6),(12,8),
    (14,3),(14,11)
]

LETTER_VALUES = {
    "a": 1, "b": 3, "c": 3, "d": 2,
    "e": 1, "f": 4, "g": 2, "h": 4,
    "i": 1, "j": 8, "k": 5, "l": 1,
    "m": 3, "n": 1, "o": 1, "p": 3,
    "q": 10, "r": 1, "s": 1, "t": 1,
    "u": 1, "v": 4, "w": 4, "x": 8,
    "y": 4, "z": 10
}


class Board:
    def __init__(self):
        self.size = 15
        self.grid = [[None]*self.size for _ in range(self.size)]
        self.multipliers = self.__init__multipliers()

    def __init__multipliers(self) -> list:
        """Sets up multiplier representation layer on given grid."""
        multipliers = [[None]*self.size for _ in range(self.size)]
        for r,c in TRIPLE_WORD:
            multipliers[r][c] = "TW"
        for r,c in DOUBLE_WORD:
            multipliers[r][c] = "DW"
        for r,c in TRIPLE_LETTER:
            multipliers[r][c] = "TL"
        for r,c in DOUBLE_LETTER:
            multipliers[r][c] = "DL"
        return multipliers
    
    def load_board(self, board_state) -> None:
        """Loads a given board state into the grid.
        board_state should be a list of 15 lists, each containing 15 sets (or Nones):
        (char, is_blank_tile) where char is the letter and is_blank_tile is a boolean."""
        self.validate_board_state(board_state)
        for r in range(self.size):
            for c in range(self.size):
                if board_state[r][c] is not None:
                    char, is_blank_tile = board_state[r][c]
                    self.grid[r][c] = (char, is_blank_tile)
                else:
                    self.grid[r][c] = None
    
    def validate_board_state(self, board_state) -> bool:
        """Validates board state size and cell formats."""
        for r in range(len(board_state)):
            for c in range(len(board_state[r])):
                if (r >= self.size) or (c >= self.size):
                    raise ValueError(f"Board state exceeds board dimensions at position ({r},{c}). Expected dimensions: {self.size}x{self.size}.")
                if (board_state[r][c] is not None) and not (isinstance(board_state[r][c], tuple) and len(board_state[r][c]) == 2 and isinstance(board_state[r][c][0], str) and isinstance(board_state[r][c][1], bool)):
                    raise ValueError(f"Invalid board state at position ({r},{c}). Each cell must be None or a tuple(char, is_blank_tile).")
                
    def is_empty(self) -> bool:
        """Returns True if board is empty, False otherwise."""
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] is not None:
                    return False
        return True
    
    def find_anchors(self) -> set:
        """Finds anchor points on the board.
        An ancor point is an empty cell adjacent to an occupied cell, or the center if board is empty.
        Returns a set of (row,col) tuples."""
        if self.is_empty():
            return {(7, 7)}
        anchors = set()
        for r in range(self.size):
            for c in range(self.size):
                # Case: not board edge cell
                if self.grid[r][c] is not None and 0 < r < self.size - 1 and 0 < c < self.size - 1:
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if (dr != 0 or dc != 0) and self.grid[r+dr][c+dc] is None:
                                anchors.add((r+dr, c+dc))
                # Case: top edge, non corner cell
                elif self.grid[r][c] is not None and r == 0 and 0 < c < self.size - 1:
                    for dr in [0, 1]:
                        for dc in [-1, 0, 1]:
                            if (dr != 0 or dc != 0) and self.grid[r+dr][c+dc] is None:
                                anchors.add((r+dr, c+dc))
                # Case: bottom edge, non corner cell
                elif self.grid[r][c] is not None and r == self.size - 1 and 0 < c < self.size - 1:
                    for dr in [-1, 0]:
                        for dc in [-1, 0, 1]:
                            if (dr != 0 or dc != 0) and self.grid[r+dr][c+dc] is None:
                                anchors.add((r+dr, c+dc))
                # Case: left edge, non corner cell
                elif self.grid[r][c] is not None and 0 < r < self.size - 1 and c == 0:
                    for dr in [-1, 0, 1]:
                        for dc in [0, 1]:
                            if (dr != 0 or dc != 0) and self.grid[r+dr][c+dc] is None:
                                anchors.add((r+dr, c+dc))
                # Case: right edge, non corner cell
                elif self.grid[r][c] is not None and 0 < r < self.size - 1 and c == self.size - 1:
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0]:
                            if (dr != 0 or dc != 0) and self.grid[r+dr][c+dc] is None:
                                anchors.add((r+dr, c+dc))
                # Case: top left corner
                elif self.grid[r][c] is not None and r == 0 and c == 0:
                    for dr in [0, 1]:
                        for dc in [0, 1]:
                            if (dr != 0 or dc != 0) and self.grid[r+dr][c+dc] is None:
                                anchors.add((r+dr, c+dc))
                # Case: top right corner
                elif self.grid[r][c] is not None and r == 0 and c == self.size - 1:
                    for dr in [0, 1]:
                        for dc in [-1, 0, 1]:
                            if (dr != 0 or dc != 0) and self.grid[r+dr][c+dc] is None:
                                anchors.add((r+dr, c+dc))
                # Case: bottom left corner
                elif self.grid[r][c] is not None and r == self.size - 1 and c == 0:
                    for dr in [-1, 0]:
                        for dc in [0, 1]:
                            if (dr != 0 or dc != 0) and self.grid[r+dr][c+dc] is None:
                                anchors.add((r+dr, c+dc))
                # Case: bottom right corner
                elif self.grid[r][c] is not None and r == self.size - 1 and c == self.size - 1:
                    for dr in [-1, 0]:
                        for dc in [-1, 0, 1]:
                            if (dr != 0 or dc != 0) and self.grid[r+dr][c+dc] is None:
                                anchors.add((r+dr, c+dc))
        return anchors
