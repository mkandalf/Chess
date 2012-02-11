from itertools import product


class Piece(object):
  """Abstract base class for pieces."""
  def __init__(self, owner, location):
    self.owner = owner
    self.x, self.y = location

  @property
  def location(self):
    return self.x, self.y

  def reachable(self, board):
    """Get all the square reachable from the piece's current location."""
    raise NotImplemented

  def moves(self, board):
    """Get all the possible moves for the piece."""
    for square in self.reachable(board):
      yield Move(self, square)

  def can_reach(self, board, square):
    """Check if the given square is reachable."""
    for reachable_square in self.reachable(board):
      if reachable_square == square:
        return True
    return False


class Pawn(Piece):
  pass


class Bishop(Piece):
  pass


class Knight(Piece):
  pass


class Rook(Piece):
  pass


class King(Piece):
  def reachable(self, board):
    for x, y in product(range(-1, 2), range(-1, 2)):
      if not (x == y == 0):
        to = new_x, new_y = (self.x + x, self.y + y)
        if 7 >= new_x >= 0 and 7 >= new_y >= 0:
          piece = board.piece_at(to)
          if piece is None or piece.owner != self.owner:
            yield to


class Queen(Piece):
  pass
