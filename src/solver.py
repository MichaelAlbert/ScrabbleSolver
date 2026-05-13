from trie import build_trie_from_file, Trie
from rack import Rack
from board import Board

class SolveState:
    def __init__(self, dictionary, rack, board):
        self.dictionary = dictionary
        self.rack = rack
        self.board = board
    
    def find_top_moves(self, n=10):
        """Finds the top n moves based on current board and rack state."""
        # This would involve generating all valid moves, scoring them, and returning the top n
        return self.score_moves(self.generate_moves())[:n]
    
    def generate_moves(self):
        """Generates all valid moves based on current board and rack state."""
        anchors = self.board.find_anchors()
        moves = {}