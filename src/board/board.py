import numpy as np

from bitboard import Bitboard

import constants
from constants import magic_number_rook, magic_number_bishop, magic_number_shifts_rook, magic_number_shifts_bishop, occupancy_mask_rook, occupancy_mask_bishop, rook_moves


#TODO: Why do we start at 2? Or- why do we encode pieces starting at 0 in Move?
EMPTY = 2
PAWN = 3
KNIGHT = 4
BISHOP = 5
ROOK = 6
QUEEN = 7
KING = 8

rooks = [[0, 56], [1, 57], [2, 58], [3, 59],
    [4, 60], [5, 61], [6, 62], [7, 63]]

class Piece(np.uint8):
  #Not sure this will be needed..
  pass


class Move(np.uint16):
  """A move is a 16-bit integer representing an arc from one position to another.

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
  @property
  def promoted(self):
    return self >> 16

  @property
  def piece(self):
    return (self >> 12) & 7

  @property
  def head(self):
    """The encoded destination square."""
    return self >> 6 & 63

  @property
  def tail(self):
    """The encoded departure square."""
    return self & 63

  def __repr__(self):
    raw = np.binary_repr(self).zfill(16)
    return " ".join((raw[0], raw[1:4], raw[4:10], raw[10:16]))


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
  PIECE_INIT = (
      np.uint64(0xFFFF),
      np.uint64(0xFFFF000000000000),
      np.uint64(0x0000ffffffff0000),
      np.uint64(0x00ff00000000ff00),
      np.uint64(0x4200000000000024),
      np.uint64(0x2400000000000042),
      np.uint64(0x8100000000000018),
      np.uint64(0x1000000000000010),
      np.uint64(0x0800000000000008))
  OCCUPIED_INIT = np.uint64(0xffff00000000ffff)
  EMPTY_INIT = np.uint64(0x0000ffffffff0000)

  def __init__(self):
    # status - 50-move, en-passant, color to move, castling rights
    self.status = np.uint16(0)
    self.side_to_move = np.bool()
    #TODO: Why is this? Shouldn't this just be 4 bits? / Isn't this take care of in status?
    self.castling_rights = [[3,3]] * 67

    #TODO: Why is this needed?
    self.king_square = [4, 60]
    #TODO: This can actually be replaced by a huffman encoding
    #TODO: More so, we can XOR with the starting position
    self.piece_square = [
        6, 4, 5, 7, 8, 5, 4, 6,
        3, 3, 3, 3, 3, 3, 3, 3,
        2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2,
        3, 3, 3, 3, 3, 3, 3, 3,
        6, 4, 5, 7, 8, 5, 4, 6]


    #TODO: Document what's going on here.
    # makeMove does not validate moves (e.g castling without rights)
    def make_move(self, move):
      #parse an encoded move
      piece = move.piece + 2 #arbitrary
      p_to = move.to
      p_from = move.from_
      captured = move.captured
      promoted = move.promoted

      #put the move in context of the board
      from_BB = np.uint64(1) << p_from 
      to_BB = np.uint64(1) << p_to 
      from_to_BB = from_BB ^ to_BB

      self.piece_BB[piece] ^= from_to_BB
      self.piece_BB[side_to_move] ^= from_to_BB 
      self.piece_square[p_from] = EMPTY
      self.piece_square[p_to] = piece

      if piece == KING:
        self.king_square[side_to_move] = p_to
        if self.castle[ply][side_to_move] > 0:
          if abs(p_to - p_from) == 2:
            if p_to == rooks[6][side_to_move]:
              p_from = rooks[7][side_to_move]
              p_to = rooks[5][side_to_move]
            else:
              p_from = rooks[0][side_to_move]
              p_to = rooks[3][side_to_move]
            rook_bitmap = np.uint64(1) << p_from | np.uint64(1) << p_to
            self.piece_BB[ROOK] ^= rook_bitmap
            self.piece_BB[side_to_move] ^= rook_bitmap
            self.piece_square[p_from] = EMPTY
            self.piece_square[p_to] = ROOK
      elif piece == PAWN:
        # Add en passant
        if promoted:
          promoted += 2
          self.piece_BB[piece] ^= to_BB 
          self.piece_BB[promoted] ^= to_BB
      elif piece == ROOK :
        if self.castle[ply][side_to_move] > 0:
          if p_from == rooks[7][side_to_move]:
            self.castle[ply][side_to_move] &= 1
          elif p_from == rooks[0][side_to_move]:
            self.castle[ply][side_to_move] &= 2

      if captured:
        captured += 2
        self.piece_BB[captured] ^= to_BB                  
        self.piece_BB[self.flip(side_to_move)] ^= to_BB
        self.occupied_BB ^= from_BB 
        self.empty_BB ^= from_BB
      else:
        self.occupied_BB ^= from_to_BB 
        self.empty_BB ^= from_to_BB


# TODO: Check detection, pawn promotion captures, sliding pieces

  def gen_moves(board):
    """Generate the set of all possible moves."""
    moves = set()
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
