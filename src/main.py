from board import Board
from rack import Rack
from solver import SolveState
from trie import build_trie_from_file, Trie

def main():
    # Initialize board, rack, and trie
    board = Board("crossplay")
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
        [None,None,None,None,None,None,None,None,None,None,('q', False),None,None,None,None],
        [None,None,None,None,None,None,None,('t', False),None,None,('u', False),None,None,None,None],
        [None,None,None,None,None,None,('s', False),('h', False),('a', False),('v', False),('e', False),('d', False),None,None,None],
        [None,None,None,None,None,None,None,('i', False),None,None,('e', False),None,None,None,None],
        [None,None,None,None,None,None,None,('t', False),None,None,('n', False),None,None,None,None],
        [None,None,None,None,None,None,('c', False),('h', False),('a', False),('w', False),('s', False),None,None,None,None],
        [None,None,None,None,None,('s', True),None,('e', False),None,None,None,None,None,None,None],
        [None,None,None,None,None,('w', False),('a', False),('r', False),None,None,None,None,None,None,None],
        [None,None,None,None,None,('a', False),('x', False),None,None,None,None,None,None,None,None],
        [None,None,('t', False),('h', False),('e', False),('m', False),('e', False),None,None,None,None,None,None,None,None],
    ]
    rack.fill_rack("to.waio")
    board.load_board(board_state)                                                                                       

    # Initialize solve state and find top 10 moves
    solve_state = SolveState(trie, rack, board)
    solve_state.generate_moves()
    top_ten_moves = solve_state.find_top_moves(10)
    solve_state.print_moves(top_ten_moves, 10)
    board.print_board()
    board.preview_move(top_ten_moves[0])
    # print(solve_state.find_existing_prefix((8,9),1,0)) # debug
    # print(solve_state.find_limit((8,9),1,0)) # debug

if __name__ == "__main__":
    main()