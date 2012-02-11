

class Piece(object):
  """Abstract base class for pieces."""
  def __init__(self, owner, location):
    self.owner = owner
    self.y, self.x = location

  @property
  def location(self):
    return self.y, self.x

  @property
  def moves(self):
    """Get all the legal moves for the piece."""
    raise NotImplemented

  def is_legal(self, move):
    """Check if the given move is legal."""
    return move in self.moves


class Pawn(Piece):
  pass

class Bishop(Piece):
  pass

class Knight(Piece):
  pass

class Rook(Piece):
  pass

class King(Piece):
  pass

class Queen(Piece):
  pass
