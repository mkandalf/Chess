from numpy import uint64
from board import EMPTY, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING

def gen_moves(board):
    # King, Knight are simple
    # Pawns are also relatively easy, some bit shifting
    # Sliding pieces - magic bitboards and hashes

def gen_king_moves(board):
    king = board.piece_BB[KING] & boad.piece_BB[board.to_move] 
    attacks = east_one(king) | west_one(king)
    king |= attacks
    attacks |= north_one(king) | south_one(king)

def gen_pawn_moves(board):
    pass

def gen_knight_moves(board):
    pass

def east_one(a):
    a << 1

def west_one(a):
    a >> 1

def north_one(a):
    a << 8

def south_one(a):
    a >> 8

def no_ea_one(a):
    a << 9

def so_ea_one(a):
    a >> 7

def no_we_one(a):
    a << 7

def so_we_one(a):
    a >> 9
