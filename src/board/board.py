from numpy import uint64, uint16

PIECE_INIT = [
    uint64(0xFFFF),
    uint64(0xFFFF000000000000),
    uint64(0x0000ffffffff0000),
    uint64(0x00ff00000000ff00),
    uint64(0x4200000000000024),
    uint64(0x2400000000000042),
    uint64(0x8100000000000018),
    uint64(0x1000000000000010),
    uint64(0x0800000000000008)]
OCCUPIED_INIT = uint64(0xffff00000000ffff)
EMPTY_INIT = uint64(0x0000ffffffff0000)

EMPTY = 2
PAWN = 3
KNIGHT = 4
BISHOP = 5
ROOK = 6
QUEEN = 7
KING = 8

rooks = [[0, 56], [1, 57], [2, 58], [3, 59],
    [4, 60], [5, 61], [6, 62], [7, 63]]


class Board(object):
  def __init__(self):
    # It will probably provide a speed up to eventually track
    # # of majors, minors, material count, etc, here.
    self.piece_BB = PIECE_INIT
    self.occupied_BB = OCCUPIED_INIT
    self.empty_BB = EMPTY_INIT

    # status - 50-move, en-passant, color to move, castling rights
    self.status = uint16(0)
    self.side_to_move = 0
    self.castling_rights = [[3,3]] * 67
    self.king_square = [4, 60]
    self.piece_square = [
        6, 4, 5, 7, 8, 5, 4, 6,
        3, 3, 3, 3, 3, 3, 3, 3,
        2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2,
        3, 3, 3, 3, 3, 3, 3, 3,
        6, 4, 5, 7, 8, 5, 4, 6]


    # makeMove does not validate moves (e.g castling without rights)
    def make_move(self, move, ply, side_to_move):
      piece = move.piece + 2
      p_to = move.to
      p_from = move.from_
      captured = move.captured
      promoted = move.promoted

      from_BB = uint64(1) << p_from 
      to_BB = uint64(1) << p_to 
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
            rook_bitmap = uint64(1) << p_from | uint64(1) << p_to
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
