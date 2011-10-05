import constants

def gen_moves(board):
    constants.init()
    # King, Knight are simple
    # Pawns are also relatively easy, some bit shifting
    # Sliding pieces - magic bitboards and hashes

def gen_king_moves(board):
    king_index = board.king_square[board.to_move] 
    return constants.all_king_attacks[king_index] \
            & ~board.piece_BB[board.to_move] 

def gen_pawn_moves(board):
    pass

def gen_knight_moves(board):
    pass
























