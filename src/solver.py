from trie import build_trie_from_file, Trie
from rack import Rack
from board import Board
from copy import deepcopy

class SolveState:
    def __init__(self, dictionary: Trie, rack: Rack, board: Board):
        self.dictionary = dictionary
        self.rack = rack
        self.board = board
        self.anchors = set()
        self.moves = {}
    
    def find_top_moves(self, n=10) -> list:
        """Finds the top n moves based on current board and rack state."""
        # This would involve generating all valid moves, scoring them, and returning the top n
        return 1
    
    def generate_moves(self) -> None:
        """Generates all valid moves based on current board and rack state."""
        self.anchors = self.board.find_anchors()
        for anchor in self.anchors:
            for dr, dc in [(0, 1), (1, 0)]: # Horizontal and vertical directions
                limit = self.find_limit(anchor, dr, dc)
                self.left_part(anchor, "", self.dictionary.root, deepcopy(self.rack), deepcopy(self.rack), dr, dc, limit)
            return

    def left_part(self, anchor, partial_word, node, rack_remaining, rack_used, dr, dc, limit) -> None:
        """Recursively builds valid left parts of a word starting from an anchor point.
        partial_word is the current string being built,
        node is the current TrieNode,
        rack_remaining is the number of letters left in the rack,
        rack_used is a set of letters already used from the rack,
        r and c are the current row and column on the board,
        dr and dc represent the direction of the main word being formed,
        cell is the current board cell being considered."""
        # Attempt right expansion from current partial to find valid moves
        self.extend_right(partial_word, node, anchor, rack_remaining, rack_used, dr, dc)
        # Base case: limit reached
        if limit <0:
            return
        
        for char in node.children:
            used_char, is_blank = rack_remaining.use_letter(char)
            rack_used.restore_letter(char, is_blank)
            if used_char:
                self.left_part(anchor, partial_word + char, node.children[char], rack_remaining, rack_used, dr, dc, limit - 1)
                rack_remaining.restore_letter(char, is_blank)
                rack_used.use_letter(char)

    def extend_right(self, partial_word, node, cell, rack_remaining, rack_used, dr, dc) -> None:
        """Recursively extends the current partial word to the right to find valid moves.
        Similar parameters as left_part but without limit."""
        if self.board.grid[cell[0]][cell[1]] is None:
            if node.is_word:
                self.moves[partial_word] = {"score": 0, "end": (cell[0] - dr, cell[1] - dc), "direction": (dr,dc)}
            for char in node.children:
                used_char, is_blank = rack_remaining.use_letter(char)
                rack_used.restore_letter(char, is_blank)
                if used_char:
                    self.extend_right(partial_word + char, node.children[char], (cell[0] + dr, cell[1] + dc), rack_remaining, rack_used, dr, dc)
                    rack_remaining.restore_letter(char, is_blank)
                    rack_used.use_letter(char)
        else:
            char = self.board.grid[cell[0]][cell[1]][0]
            if char in node.children:
                next_node = node.children[char]
                next_cell = (cell[0] + dr, cell[1] + dc)
                self.extend_right(partial_word + char, next_node, next_cell, rack_remaining, rack_used, dr, dc)

    def check_crossword(self, cell, letter, dr, dc) -> bool:
        """Checks for crossword validity when placing a given letter at a given cell.
        dr and dc represent the direction of the main word being formed (e.g. dr=0, dc=1 for horizontal)."""
        word = letter
        r, c = cell
        while 1 <= r < 15 and 1 <= c < 15 and self.board.grid[r-dr][c-dc] is not None and dr == 1: # Vertical case
            word = self.board.grid[r-dr][c-dc][0] + word # Prepend existing letter to word
            r -= dr
        r, c = cell
        while 1 <= r < 15 and 1 <= c < 15 and self.board.grid[r-dr][c-dc] is not None and dr == 1: # Vertical case
            word += self.board.grid[r-dr][c-dc][0] # Append existing letter to word
            r -= dr

        r, c = cell
        while 1 <= r < 15 and 1 <= c < 15 and self.board.grid[r-dr][c-dc] is not None and dc == 1: # Horizontal case
            word = self.board.grid[r-dr][c-dc][0] + word # Prepend existing letter to word
            c -= dc
        r, c = cell
        while 1 <= r < 15 and 1 <= c < 15 and self.board.grid[r-dr][c-dc] is not None and dc == 1: # Horizontal case
            word += self.board.grid[r-dr][c-dc][0] # Append existing letter to word
            c -= dc
        return self.dictionary.is_word(word)
        
    def find_crosswords(self, move) -> list:
        """Finds any crosswords formed by a given move and checks their validity.
        Returns a list of valid crosswords formed."""
        crosswords = []
        for i in range(len(move['word']) - 1, -1, -1):
            char = move['word'][i]
            dr = move['direction'][1]
            dc = move['direction'][0]
            r = move['end'][0] - i * dr
            c = move['end'][1] - i * dc
            if not self.check_crossword((r, c), char, dc, dr):
                return [-1] # Invalid crossword found, return immediately
            while 1 <= r < 15 and 1 <= c < 15 and self.board.grid[r-dr][c-dc] is not None:
                word = self.board.grid[r-dr][c-dc][0] + word # Prepend existing letter to word
                r -= dr
                c -= dc
            while 1 <= r < 15 and 1 <= c < 15 and self.board.grid[r-dr][c-dc] is not None:
                word += self.board.grid[r-dr][c-dc][0] # Append existing letter to word
                c += dc
                r += dr

            end = (r,c)
            
            if self.dictionary.is_word(word):
                crosswords.append({"word": word, "end": end})
        return crosswords

    def find_multipliers(self, move) -> dict:
        """Finds the multipliers that apply to a given move based on current board state.
        Returns a dictionary of multipliers (e.g. {'DL': (0,1), 'TW': (3,1)}) that apply to the move."""
        multipliers = {}

        for i in range(len(move['word'])):
            r = move['end'][0] - i * move['direction'][0]
            c = move['end'][1] - i * move['direction'][1]
            if self.board.grid[r][c] is None: # Only consider multipliers for newly placed tiles
                if self.board.multipliers[r][c] is not None:
                    multipliers[(r, c)] = self.board.multipliers[r][c]
        return multipliers
    
    def score_moves(self, moves):
        """Scores each move based on current board state and Scrabble scoring.
        Returns a list of moves sorted in descending order by score."""
        scored_moves = []
        for move in moves:
            if self.find_crosswords(move) == [-1]:
                self.moves.pop(move) # Skip moves that create invalid crosswords
            multipliers = self.find_multipliers(move)
            score = 0
            for i in range(len(move['word']) - 1, -1, -1):
                char = move['word'][i]
                char_score = Board.LETTER_SCORES[char] if char in Board.LETTER_SCORES else 0
                r = move['end'][0] - i * move['direction'][0]
                c = move['end'][1] - i * move['direction'][1]
                if (r, c) in multipliers:
                    if multipliers[(r, c)] == 'DL':
                        char_score *= 2
                    elif multipliers[(r, c)] == 'TL':
                        char_score *= 3
                score += char_score
            for multiplier in multipliers.values():
                if multiplier == 'DW':
                    score *= 2
                elif multiplier == 'TW':
                    score *= 3
            for crossword in self.find_crosswords(move):
                for i in range(len(crossword['word']) - 1, -1, -1):
                    char = crossword['word'][i]
                    char_score = Board.LETTER_SCORES[char] if char in Board.LETTER_SCORES else 0
                    r = crossword['end'][0] - i * move['direction'][1]
                    c = crossword['end'][1] - i * move['direction'][0]
                    if (r, c) in multipliers and self.board.grid[r][c] is None: # Only apply multipliers to newly placed tiles
                        if multipliers[(r, c)] == 'DL':
                            char_score *= 2
                        elif multipliers[(r, c)] == 'TL':
                            char_score *= 3
                    cross_score += char_score
                if (r, c) in multipliers and self.board.grid[r][c] is None: # Only apply multipliers to newly placed tiles
                    if multipliers[(r, c)] == 'DW':
                        cross_score *= 2
                    elif multipliers[(r, c)] == 'TW':
                        cross_score *= 3
                    score += cross_score
                    cross_score = 0
                    char_score = 0
            self.moves[move]['score'] = score
            scored_moves.append(self.moves[move])
        return sorted(scored_moves, key=lambda x: x["score"], reverse=True)
    
    def find_limit(self, anchor, dr, dc) -> int:
        """Finds the limit for left part generation (number of open squares "left" of given anchor)"""
        r, c = anchor
        limit = 0
        # Ignore anchor cell
        r -= dr
        c -= dc
        while 1 <= r < self.board.size and 1 <= c < self.board.size and self.board.grid[r][c] is None:
            limit += 1
            r -= dr
            c -= dc
        return limit