from trie import build_trie_from_file, Trie
from rack import Rack
from board import Board, LETTER_VALUES
from copy import deepcopy

class SolveState:
    def __init__(self, dictionary: Trie, rack: Rack, board: Board):
        self.dictionary = dictionary
        self.rack = rack
        self.board = board
        self.anchors = set()
        self.moves = []
        self.seen_moves = set()
    
    def find_top_moves(self, n=10) -> list:
        """Finds the top n moves based on current board and rack state."""
        return self.score_moves()[:n]
    
    def generate_moves(self) -> None:
        """Generates all valid moves based on current board and rack state."""
        self.anchors = self.board.find_anchors()
        for anchor in self.anchors:
            for dr, dc in [(0, 1), (1, 0)]: # Horizontal and vertical directions
                limit = self.find_limit(anchor, dr, dc)
                if limit == 0:
                    prefix, node = self.find_existing_prefix(anchor, dr, dc).values()
                    if node is not None:
                        self.extend_right(prefix, node, anchor, deepcopy(self.rack), dr, dc)
                else:
                    self.left_part(anchor, "", self.dictionary.root, deepcopy(self.rack), dr, dc, limit)
        #print("Generated moves:", self.moves) # Debug

    def left_part(self, anchor, partial_word, node, rack, dr, dc, limit) -> None:
        """Recursively builds valid left parts of a word starting from an anchor point.
        partial_word is the current string being built,
        node is the current TrieNode,
        rack_remaining is the number of letters left in the rack,
        rack_used is a set of letters already used from the rack,
        r and c are the current row and column on the board,
        dr and dc represent the direction of the main word being formed,
        cell is the current board cell being considered."""
        # Attempt right expansion from current partial to find valid moves
        self.extend_right(partial_word, node, anchor, rack, dr, dc)
        # Base case: limit reached
        if limit <=0:
            return
        
        for char in node.children:
            used_char, is_blank = rack.use_letter(char)
            if used_char:
                self.left_part(anchor, partial_word + char, node.children[char], rack, dr, dc, limit - 1)
                rack.restore_letter(char, is_blank) 

    def extend_right(self, partial_word, node, cell, rack, dr, dc) -> None:
        """Recursively extends the current partial word to the right to find valid moves.
        Similar parameters as left_part but without limit."""
        r, c = cell
        # Bounds check
        if not (0 <= r < self.board.size and 0 <= c < self.board.size):
            return
        if self.board.grid[r][c] is None:
            if node.is_word:
                move = {"word": partial_word, "score": 0, "end": (cell[0] - dr, cell[1] - dc), "direction": (dr,dc)}
                cross = self.find_crosswords(move)
                if cross == [-1]:
                    return # Invalid crossword found, skip move
                if not self.move_touches_existing_tile(move):
                    return # Skip moves that don't touch existing tiles
                move_key = self.move_key(move)
                if move_key not in self.seen_moves:
                    self.seen_moves.add(move_key)
                    self.moves.append(move)
            for char in node.children:
                used_char, is_blank = rack.use_letter(char)
                if used_char:
                    self.extend_right(partial_word + char, node.children[char], (cell[0] + dr, cell[1] + dc), rack, dr, dc)
                    rack.restore_letter(char, is_blank)

        else:
            char = self.board.grid[r][c][0]
            if char in node.children:
                next_node = node.children[char]
                next_cell = (r + dr, c + dc)
                self.extend_right(partial_word + char, next_node, next_cell, rack, dr, dc)

    def check_crossword(self, cell, letter, dr, dc) -> bool:
        """Checks for crossword validity when placing a given letter at a given cell.
        dr and dc represent the direction of the main word being formed (e.g. dr=0, dc=1 for horizontal)."""
        word = letter
        r, c = cell
        pr, pc = dc, dr # Perpendicular direction for crossword checking

        rr, cc = r - pr, c - pc
        while 0 <= rr < self.board.size and 0 <= cc < self.board.size and self.board.grid[rr][cc] is not None:
            word = self.board.grid[rr][cc][0] + word # Prepend existing letter to word
            rr -= pr
            cc -= pc

        rr, cc = r + pr, c + pc
        while 0 <= rr < self.board.size and 0 <= cc < self.board.size and self.board.grid[rr][cc] is not None:
            word += self.board.grid[rr][cc][0] # Append existing letter to word
            rr += pr
            cc += pc
        
        if len(word) == 1:
            return True
        return self.dictionary.is_word(word)
    
        
    def find_crosswords(self, move) -> list:
        """Finds any crosswords formed by a given move and checks their validity.
        Returns a list of valid crosswords formed."""
        crosswords = []
        dr, dc = move['direction']
        for i in range(len(move['word'])):
            char = move['word'][i]
            word = char
            self.find_start(move)
            r = move['start'][0] +i * dr
            c = move['start'][1] + i * dc
            if self.board.grid[r][c] is not None:
                continue # Don't crossword check existing tiles
            if not self.check_crossword((r, c), char, dr, dc):
                return [-1] # Invalid crossword found, return immediately
            pr, pc = dc, dr # Perpendicular direction for crossword checking
            rr, cc = r - pr, c - pc
            while 0 <= rr < self.board.size and 0 <= cc < self.board.size and self.board.grid[rr][cc] is not None:
                word = self.board.grid[rr][cc][0] + word # Prepend existing letter to word
                rr -= pr
                cc -= pc
            rr, cc = r + pr, c + pc
            while 0 <= rr < self.board.size and 0 <= cc < self.board.size and self.board.grid[rr][cc] is not None:
                word += self.board.grid[rr][cc][0] # Append existing letter to word
                rr += pr
                cc += pc
                

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
    
    def score_moves(self) -> list:
        """Scores each move based on current board state and Scrabble scoring.
        Returns a list of moves sorted in descending order by score."""
        scored_moves = []
        for move in self.moves:
            if self.find_crosswords(move) == [-1] or not self.validate_placed(move):
                #print(f"debug bad move: {move}") # Debug
                continue
            multipliers = self.find_multipliers(move)
            cross_score = 0
            score = 0
            for i in range(len(move['word']) - 1, -1, -1):
                char = move['word'][i]
                r = move['end'][0] - i * move['direction'][0]
                c = move['end'][1] - i * move['direction'][1]
                if self.board.grid[r][c] is not None and self.board.grid[r][c][1]:
                    char_score = 0 # Blank tile
                else:
                    char_score = LETTER_VALUES[char] if char in LETTER_VALUES else 0
                if (r, c) in multipliers and self.board.grid[r][c] is None: # Only apply multipliers to newly placed tiles
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
            #print(f"Base score for move {move}: {score}") # Debug
            for crossword in self.find_crosswords(move):
                #print(f"Word: {move}") # Debug
                #print(f"Crossword found: {crossword}") # Debug
                for i in range(len(crossword['word']) - 1, -1, -1):
                    char = crossword['word'][i]
                    char_score = LETTER_VALUES[char] if char in LETTER_VALUES else 0
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
            move['score'] = score
            scored_moves.append(move)
            #print(f"MOOOOOOOOOOVE: {move}") # Debug
            #print(f"Score: {score}") # Debug")
        #print("Scored moves:", scored_moves) #debug 
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
        #print(limit) # Debug
        return limit
    
    def find_existing_prefix(self, anchor, dr, dc) -> dict:
        """Used when "left" of anchor is occupied. Finds the existing prefix string in that direction."""
        r, c = anchor
        prefix = ""
        # Move in the specified direction until we hit the edge or an empty cell
        r -= dr
        c -= dc
        while 0 <= r < self.board.size and 0 <= c < self.board.size and self.board.grid[r][c] is not None:
            char, _ = self.board.grid[r][c]
            prefix = char + prefix
            r -= dr
            c -= dc
        return {"prefix": prefix, "node": self.dictionary.search(prefix)}
    
    def validate_placed(self, move) -> bool:
        """Validates that a move contains at least one new tile."""
        for i in range(len(move['word'])):
            r = move['end'][0] - i * move['direction'][0]
            c = move['end'][1] - i * move['direction'][1]
            if self.board.grid[r][c] is None:
                return True
        return False
    
    def print_moves(self, moves, n) -> None:
        print(f"Top {n} Moves:")
        print("-" * 50)
        for i, m in enumerate(moves, 1):
            print(
                f"{i:2d}. {m['word']:<10} "
                f"Score: {m['score']:<3} "
                f"Start: {m['start']} "
                f"End: {m['end']} "
                f"Dir: {m['direction']}"
            )
    
    def move_key(self, move) -> tuple:
        """
        Creates a canonical representation of a move based on board placement,
        not word string.
        """

        word = move['word']
        r, c = move['end']
        dr, dc = move['direction']

        placements = []

        for i in range(len(word)):
            rr = r - i * dr
            cc = c - i * dc

            # Only include NEW tiles (not pre-existing board tiles)
            if self.board.grid[rr][cc] is None:
                placements.append((rr, cc, word[i]))

        # sort so order doesn't matter
        placements.sort()

        return (tuple(placements), move['direction'])
    
    def move_touches_existing_tile(self, move) -> bool:
        """
        Returns True if at least one newly placed tile
        touches an existing board tile.
        """

        dr, dc = move['direction']

        for i, ch in enumerate(move['word']):

            r = move['end'][0] - i * dr
            c = move['end'][1] - i * dc

            # only consider newly placed tiles
            if self.board.grid[r][c] is not None:
                continue

            # orthogonal neighbors
            for nr, nc in [
                (r-1, c),
                (r+1, c),
                (r, c-1),
                (r, c+1)
            ]:
                if (
                    0 <= nr < self.board.size and
                    0 <= nc < self.board.size and
                    self.board.grid[nr][nc] is not None
                ):
                    return True

        return False
    
    def find_start(self, move) -> None:
        """Finds starting cell of a given move and adds it."""
        r = move["end"][0] - (len(move["word"]) - 1) * move["direction"][0]
        c = move["end"][1] - (len(move["word"]) - 1) * move["direction"][1]
        move["start"] = (r, c)
        