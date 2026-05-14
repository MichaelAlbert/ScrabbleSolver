from board import Board
from rack import Rack
from solver import SolveState
from trie import build_trie_from_file, Trie

def main():
    # Initialize board, rack, and trie
    board = Board()
    rack = Rack()
    trie = build_trie_from_file("words.txt")

    # Example board and rack setup
    # Will be replaced by actual input handling
    board_state = [
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,('t',False),('r',False),('a',True),('i',False),('n',False),None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
    ]
    rack.fill_rack("trains.")
    board.load_board(board_state)

    # Initialize solve state and find top 10 moves
    solve_state = SolveState(trie, rack, board)
    solve_state.generate_moves()
    top_ten_moves = solve_state.find_top_moves(10)
    solve_state.print_moves(top_ten_moves, 10)

if __name__ == "__main__":
    main()