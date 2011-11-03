from collections import namedtuple

import numpy as np

from bitboard import Bitboard
import constants
from constants import magic_number_rook, magic_number_bishop, magic_number_shifts_rook, magic_number_shifts_bishop, occupancy_mask_rook, occupancy_mask_bishop, rook_moves


#TODO: Figure out what rooks is for
rooks = [[0, 56], [1, 57], [2, 58], [3, 59],
    [4, 60], [5, 61], [6, 62], [7, 63]]

class Player():
  def __init__(self, color):
    self.color = color

"""
A move only makes sense in the context of a board. Therefore some information is encoded for us:
-Who's turn it is
-What piece is on a starting square. What piece is on an ending square.
-If the move was en passant, the piece that was captured.

A move needs to be able to store:
-Whether or not a move was a castle. If it was a castle, was it kingside or queenside? (2 bits)
-If a pawn was promoted, to what what it promoted? (3 bits)
-Was a move an en passant? (1 bit) #This could be calculated on the board side...
-Else what were the start and end squares? (12 bits)

The first bit is used to identify if a promotion has occured.
The next 3 bits store what piece the pawn was promoted to if a promotion took place.
Six bits are used to store the start and end squares since: (2 ** 6 == 64)
The next six bits store the destination square.
The last six bits store the departure square.
In short, MOVE = PROMOTION? PIECE START END

Moves mean nothing without the context of a board. Since a board is required to generate moves
their existence outside of context is implausible.
"""
Move = namedtuple('Move', ['start', 'end' 'piece', 'captured', 'promoted'])

class Piece:
  """Enum type. Indicies correspond to Board.piece_BB"""
  PAWN = 0
  KNIGHT = 1
  BISHOP = 2
  ROOK = 3
  QUEEN = 4
  KING = 5

class Turn:
  """Enum type corresponding to Board.side_to_move"""
  WHITE = False
  BLACK = True

class Board(Bitboard):
  '''A chess board. Basically, a bit board with additional information.
  
  To uniquely identify a position, a board new to keep track of a few things:
  -The location of all pieces
  -Whose turn it is
  -Which en passants are possible
  -Castling rights
  -How many moves have been made since the last pawn move or capture
  -A history of all unique past positions, in order to check for three move repetition
  '''
  # It will probably provide a speed up to eventually track
  # # of majors, minors, material count, etc, here.
  PLAYER_INIT = (
      np.uint64(0x000000000000FFFF), #white
      np.uint64(0xFFFF000000000000), #black
      )
  PIECE_INIT = (
      np.uint64(0x00ff00000000ff00), #pawns
      np.uint64(0x4200000000000024), #knights
      np.uint64(0x2400000000000042), #bishops
      np.uint64(0x8100000000000018), #rooks
      np.uint64(0x1000000000000010), #queens
      np.uint64(0x0800000000000008) #kings
      )

  def __init__(self):
    self.side_to_move = np.bool()
    #the threes here denote that castling either way is legal for both sides
    self.castling_rights = (3, 3)
    #TODO: Keep track of en-passants
    self.player_bb = self.PLAYER_INIT
    self.piece_bb = self.PIECE_INIT

# TODO: For static evaluation purposes, all methods should take a side as an argument.
# TODO: Check detection, pawn promotion captures, sliding pieces

  #TODO: Abstract all of this into a single function that uses the Piece index to figure out how to generate the moves

  def moves(self, side=None):
    """Generate the set of all possible moves.

    If side is not provided, self.side_to_move is used instead."""
    moves = set()
    #TODO: Figure out what constants.init does
    #constants.init()
    # King, Knight are simple
    gen_king_moves(board)
    gen_knight_moves(board)
    gen_knight_captures(board)
    # Pawns are also relatively easy, some bit shifting
    gen_pawn_moves(board) # Includes promotions
    gen_pawn_captures(board) # Should include capturing promotions
    # Sliding pieces - magic bitboards and hashes
    return moves

  def get_moves(self, piece, color):
    """Get the set of all legal moves for a given piece."""
    assert piece in range(5) 
    if color is None:
      color = self.side_to_move
    moves = set()
    start = self.piece_bb[piece] & self.player_bb[color]
    if piece == PIECE.PAWN:
      pass
    elif piece == PIECE.KNIGHT:
      pass
    elif piece == PIECE.BISHOP:
      pass
    elif piece == PIECE.ROOK:
      pass
    elif piece == PIECE.QUEEN:
      pass
    else: #piece == PIECE.KING:
      #TODO: Handle self-check
      ends = Bitboard(constants.all_king_attacks[king_loc] & ~self.piece_bb[color])
      while ends:
        end = ends.bit_scan_forward()
        moves.add(Move(start=start, end=end,
          piece=Piece.KING, capture=False, promote=False))
        ends = ends.clear_least_bit()
    return moves

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
