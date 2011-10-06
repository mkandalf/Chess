import constants
import util
from board import KNIGHT, PAWN, KING
from numpy import uint64

def gen_moves(board):
    constants.init()
    # King, Knight are simple
    # Pawns are also relatively easy, some bit shifting
    # Sliding pieces - magic bitboards and hashes

def gen_move(p_to, p_from, piece, capture, promote):
  return uint64(((promote & 7) << 18) | ((capture & 7) << 15) \
          | (((piece - 2) & 7) << 12) \
          | ((p_to & 63) << 6) | (p_from & 63))

def gen_king_moves(board):
  # Needs to be a list of moves
  move_list = []
  king_index = board.king_square[board.to_move] 
  to = constants.all_king_attacks[king_index] \
       & ~board.piece_BB[board.to_move]
  while (to):
    move_list.append(
      gen_move(util.bit_scan_forward(to), board.king_square[board.to_move],
                KING, 0, 0))
    to = util.clear_least_bit(to)
  return move_list

def gen_pawn_moves(board):
  move_list = []
  froms = board.piece_BB[PAWN] & board.piece_BB[board.to_move]
  to = (util.south_one(froms) if board.to_move else util.north_one(froms)) \
        & board.empty_BB
  while (to):
    move_list.append(
      gen_move(util.bit_scan_forward(to), 
               util.bit_scan_forward(
                 to << uint64(8) if board.to_move else to >> uint64(8)),
                PAWN, 0, 0)) 
    to = util.clear_least_bit(to)
  return move_list

def gen_knight_moves(board):
    knights = board.piece_BB[KNIGHT] 
    while knights:
        loc = util.bit_scan_forward(knights)
        knights ^= uint64(1) << loc
        knight_moves = constants.all_knight_attacks[loc]
        # Append moves to move list
