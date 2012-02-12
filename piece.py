from itertools import product

from player import Color


class Piece(object):
    """Abstract base class for pieces."""
    def __init__(self, owner, location):
        self.owner = owner
        self.x, self.y = location

    def get_location(self):
        return self.x, self.y
    def set_location(self, value):
        self.x, self.y = value
    location = property(get_location, set_location)

    def reachable(self, board):
        """Get all the square reachable from the piece's current location."""
        raise NotImplemented

    def moves(self, board):
        """Get all the possible moves for the piece."""
        for square in self.reachable(board):
            yield Move(self, square)

    def can_reach(self, board, square):
        """Check if the given square is reachable."""
        return any(s == square for s in self.reachable(board))

    def __repr__(self):
        return "%s %s" % (self.__class__, self.location)


class Pawn(Piece):
    def reachable(self, board):
        if self.owner.color == Color.WHITE:
            vector = 1
            start_rank = 1
        else:
            vector = -1
            start_rank = 6
        forward_1 = self.x, self.y + vector
        if not board.piece_at(forward_1):
            yield forward_1
            if self.y == start_rank:
                forward_2 = self.x, self.y + vector * 2
                if not board.piece_at(forward_2):
                    yield forward_2
        attack1 = self.x - 1, self.y + vector
        piece = board.piece_at(attack1)
        if piece is not None and piece.owner != self.owner:
            yield attack1
        attack2 = self.x + 1, self.y + vector
        piece = board.piece_at(attack2)
        if piece is not None and piece.owner != self.owner:
            yield attack2


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
