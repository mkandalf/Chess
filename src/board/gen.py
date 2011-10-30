from numpy import uint64

from board import PAWN, KING, BISHOP, KNIGHT, ROOK, QUEEN
import constants
from constants import magic_number_rook, magic_number_bishop, magic_number_shifts_rook, magic_number_shifts_bishop, occupancy_mask_rook, occupancy_mask_bishop, rook_moves
import util


# TODO: Check detection, pawn promotion captures, sliding pieces

def gen_moves(board):
  constants.init()
  # King, Knight are simple
  gen_king_moves(board)
  gen_knight_moves(board)
  gen_knight_captures(board)
  # Pawns are also relatively easy, some bit shifting
  gen_pawn_moves(board) # Includes promotions
  gen_pawn_captures(board) # Should include capturing promotions
  # Sliding pieces - magic bitboards and hashes

def gen_move(p_to, p_from, piece, capture, promote):
  return uint64(((promote & 7) << 18) | ((capture & 7) << 15) \
          | (((piece - 2) & 7) << 12) \
          | ((p_to & 63) << 6) | (p_from & 63))

def gen_king_moves(board):
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
  pawn_advance_1 = \
    (util.south_one(froms) if board.to_move else util.north_one(froms)) \
    & board.empty_BB & ~constants.rank_mask[2 if board.to_move else 7]
  pawn_promotion = \
    (util.south_one(froms) if board.to_move else util.north_one(froms)) \
    & board.empty_BB & constants.rank_mask[2 if board.to_move else 7]
  pawn_advance_2 = ( util.south_one(pawn_advance_1) if board.to_move 
      else util.north_one(pawn_advance_1) ) \
      & board.empty_BB \
      & constants.pawn_advance_2_mask[board.to_move] 
  # Single pushes:
  to = pawn_advance_1
  while (to):
    move_list.append(
      gen_move(util.bit_scan_forward(to), 
               util.bit_scan_forward(
                 to << uint64(8) if board.to_move else to >> uint64(8)),
                PAWN, 0, 0)) 
    to = util.clear_least_bit(to)
  # Double pushes:
  to = pawn_advance_2
  while (to):
    move_list.append(                                                     
      gen_move(util.bit_scan_forward(to),                                 
               util.bit_scan_forward(
                 to << uint64(16) if board.to_move else to >> uint64(16)),
                PAWN, 0, 0)) 
    to = util.clear_least_bit(to) 
  return move_list
  # Promotion:
  to = pawn_promotion
  while (to):
    to_sq = util.bit_scan_forward(to)
    from_sq = to_sq << uint64(8) if board.to_move else to >> uint64(8)
    move_list.append(gen_move(to_sq, from_sq, PAWN, 0, QUEEN))
    move_list.append(gen_move(to_sq, from_sq, PAWN, 0, ROOK))
    move_list.append(gen_move(to_sq, from_sq, PAWN, 0, KNIGHT))
    move_list.append(gen_move(to_sq, from_sq, PAWN, 0, BISHOP))
    to = util.clear_least_bit(to)

def gen_pawn_captures(board):
  move_list = []
  froms = board.piece_BB[PAWN] & board.piece_BB[board.to_move]
  pawn_attacks_e = (util.so_ea_one(froms) if board.to_move 
                  else util.no_ea_one(froms)) \
                  & board.piece_BB[util.flip(board.to_move)]
  pawn_attacks_w =(util.so_we_one(froms) if board.to_move
                  else util.no_we_one(froms)) \
                  & board.piece_BB[util.flip(board.to_move)]
  to = pawn_attacks_e
  while (to):
    temp_to = util.bit_scan_forward(to)
    move_list.append(
      gen_move(temp_to,
                util.bit_scan_forward(
                  to << uint64(7) if board.to_move else to >> uint64(9)),
                PAWN, board.piece_on_square[to]-2, 0))
    to = util.clear_least_bit(to)
  to = pawn_attacks_w
  while (to):
    move_list.append(
      gen_move(util.bit_scan_forward(to),
                util.bit_scan_forward(
                  to << uint64(9) if board.to_move else to >> uint64(7)),
                PAWN, 1, 0))
    to = util.clear_least_bit(to)                                       
  return move_list

def gen_knight_moves(board):
  move_list = []
  knights = board.piece_BB[KNIGHT] 
  while knights:
    loc = util.bit_scan_forward(knights)
    knights ^= uint64(1) << loc
    to = constants.all_knight_attacks[loc] & board.empty_BB
    while (to):
      move_list.append(
        gen_move(util.bit_scan_forward(to), loc, 0, 0))
      to = util.clear_least_bit(to)
  return move_list

def gen_knight_captures(board):
  move_list = []
  knights = board.piece_BB[KNIGHT]
  while knights:
    loc = util.bit_scan_forward(knights)
    knights ^= uint64(1) << loc
    to = constants.all_knight_attacks[loc] \
          & board.piece_BB[util.flip(board.to_move)]
    while (to):
      temp_to = util.bit_scan_forward(to)
      move_list.append(
        gen_move(temp_to, loc, board.piece_on_square[temp_to] - 2, 0))
      to = util.clear_least_bit(to)
  return move_list

def gen_sliding_moves(board):
  move_list = []
  rooks = [25]
  for sq in rooks:
    index = ((board.occupied_BB & occupancy_mask_rook[sq]) \
    * magic_number_rook[sq]) \
    >> magic_number_shifts_rook[sq]
    util.print_bb(index)
    move_list.append(rook_moves[sq][index])
    util.print_bb(rook_moves[sq][index])
    
  return move_list
