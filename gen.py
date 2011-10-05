import constants
import util
from board import KNIGHT
from numpy import uint64

def gen_moves(board):
    constants.init()
    # King, Knight are simple
    # Pawns are also relatively easy, some bit shifting
    # Sliding pieces - magic bitboards and hashes

def gen_king_moves(board):
    # Needs to be a list of moves
    king_index = board.king_square[board.to_move] 
    return constants.all_king_attacks[king_index] \
            & ~board.piece_BB[board.to_move] 

def gen_pawn_moves(board):
    pass

def gen_knight_moves(board):
    knights = board.piece_BB[KNIGHT] 
    while knights:
        loc = util.bit_scan_forward(knights)
        knights ^= uint64(1) << loc
        knight_moves = constants.all_knight_attacks[loc]
        # Append moves to move list
