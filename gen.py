# To Do: Check detection, pawn promotion captures, diagonally sliding pieces
import constants
import util
from constants import magic_number_rook, \
                      magic_number_bishop, \
                      magic_number_shifts_rook, \
                      magic_number_shifts_bishop, \
                      occupancy_mask_rook, \
                      occupancy_mask_bishop, \
                      rook_moves
from board import PAWN, KING, BISHOP, KNIGHT, ROOK, QUEEN
from numpy import uint64

def gen_moves(board):
  constants.init()
  # King, Knight are simple
  gen_king_moves(board)
  gen_knight_moves(board, True, True)
  # Pawns are also relatively easy, some bit shifting
  gen_pawn_moves(board) # Includes promotions
  gen_pawn_captures(board) # Should include capturing promotions

def gen_move(p_to, p_from, piece, capture, promote):
  return uint64(((promote & 7) << 18) | ((capture & 7) << 15) \
          | (((piece - 2) & 7) << 12) \
          | ((p_to & 63) << 6) | (p_from & 63))

def gen_king_moves(board):
  move_list = []
  king_index = board.king_square[board.to_move] 
  to = (constants.all_king_attacks[king_index]
       & ~board.piece_BB[board.to_move])
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
    ((util.south_one(froms) if board.to_move else util.north_one(froms))
    & board.empty_BB & ~constants.rank_mask[2 if board.to_move else 7])
  pawn_promotion = \
    ((util.south_one(froms) if board.to_move else util.north_one(froms))
    & board.empty_BB & constants.rank_mask[2 if board.to_move else 7])
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
  if board.to_move:
    pawn_attacks_e = util.so_ea_one(froms)
    pawn_attacks_w = util.so_we_one(froms)
  else:
    pawn_attacks_e = util.no_ea_one(froms)
    pawn_attacks_w = util.no_we_one(froms)
  pawn_attacks_e &= board.piece_BB[util.flip(board.to_move)]
  pawn_attacks_w &= board.piece_BB[util.flip(board.to_move)]

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

def gen_knight_moves(board, moves, attacks):
  """Generate knight moves or attacks and return a list of pseudo-legal moves"""
  move_list = []
  knights = board.piece_BB[KNIGHT] 
  while knights:
    loc = util.bit_scan_forward(knights)
    knights ^= uint64(1) << loc
    to = constants.all_knights_attack[loc]
    if moves:
      knight_moves_bb = to & board.empty_BB
      move_list.extend(bitboard_to_moves(loc, knight_moves_bb, False, KNIGHT))
    if attacks:
      knight_attacks_bb = to & board.piece_BB[util.flip(board.to_move)]
      move_list.extend(bitboard_to_moves(loc, knight_attacks_bb, True, KNIGHT))
  return move_list

def gen_rook_moves(board, moves = True, attacks = True):
  """Generate rook moves or attacks and return a list of pseudo-legal moves"""
  # 1. Pick a rook
  # 2. Mask the relevant occupancy bits (ranks/files/diagonals)
  # 3. Multiply by a magic number to move the relevant bits together
  # 3. Shift the relevant bits to the beginning, removing the garbage bits
  # 4. Use this as an index for the pre-computed move table
  #
  #    Example:
  #    . . . . . . . .          D C B A 4 3 2 1
  #    . . . . . . E .          . . . . . . . E 
  #    . 1 . . . D . .          . . . . . . . .
  #    . . 2 . C . . . * magic  . . . . . . . .  >> (64 - 9) = index
  #    . . . * . . . . number = . . . . . . . . 
  #    . . B . 3 . . .          . . . . . . . .
  #    . A . . . 4 . .          . . . . . . . . 
  #    . . . . . . . .          . . . . . . . .
  #    Masked bits for          Now bits are 
  #    bishop on d4             consecutive

  move_list = []
  rooks = board.piece_BB[ROOK] & board.piece_BB[board.to_move]
  while rooks:
    sq = util.bit_scan_forward(rooks)
    rooks ^= uint64(1) << sq 
    index = (((board.occupied_BB & occupancy_mask_rook[sq])
      * magic_number_rook[sq])
      >> magic_number_shifts_rook[sq])
    to = uint64(rook_moves[sq][index])
    if moves:
      current_rook_moves = to & ~board.occupied_BB
      move_list.extend(bitboard_to_moves(sq, current_rook_moves, False, ROOK))
    if attacks:
      current_rook_attacks = to & board.piece_BB[util.flip(board.to_move)]
      move_list.extend(bitboard_to_moves(sq, current_rook_attacks, True, ROOK))
  return move_list

def bitboard_to_moves(origin, bitboard, attacks, piece):
  """Return a list of move objects from a bitboard of all pseudo-legal moves"""
  move_list = []
  while(bitboard):
    temp_to = util.bit_scan_forward(bitboard)
    if attacks: 
      move_list.append(
        gen_move(temp_to, origin, piece - 2, board.piece_square[temp_to] - 2, 0)
      )
    else:
      move_list.append(
        gen_move(temp_to, origin, piece - 2, 0, 0)
      )
    bitboard = util.clear_least_bit(bitboard)
  return move_list
