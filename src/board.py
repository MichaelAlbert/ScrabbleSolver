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
    "A": 1, "B": 3, "C": 3, "D": 2,
    "E": 1, "F": 4, "G": 2, "H": 4,
    "I": 1, "J": 8, "K": 5, "L": 1,
    "M": 3, "N": 1, "O": 1, "P": 3,
    "Q": 10, "R": 1, "S": 1, "T": 1,
    "U": 1, "V": 4, "W": 4, "X": 8,
    "Y": 4, "Z": 10
}


class Board:
    def __init__(self):
        self.size = 15
        self.grid = [[None]*self.size for _ in range(self.size)]
        self.multipliers = self.__init__multipliers()

    def __init__multipliers(self) -> list:
        """Sets up multiplier representation on 15x15 grid."""
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
        board_state should be a list of 15 lists, each containing 15 sets:
        (char, is_blank_tile) where char is the letter and is_blank_tile is a boolean."""
        self.validate_board_state(board_state)
        for r in range(self.size):
            for c in range(self.size):
                char, is_blank_tile = board_state[r][c]
                self.grid[r][c] = (char, is_blank_tile) if char else None
    
    def validate_board_state(self, board_state) -> bool:
        """Validates board state size and cell formats."""
        for r in range(board_state):
            for c in range(board_state[r]):
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