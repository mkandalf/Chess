

class Board(object):
  def __init__(self, pieces):
    self.pieces = pieces

  def checkmated(self, player):
    """Check if the given player is checkmated."""
    return False

  def stalemated(self, player):
    """Check if the given player is stalemated."""
    return False

  def is_over(self, player):
    """Check if the game is over for the given player."""
    return self.checkmated(player) or self.stalemated(player)

  def is_legal(self, move):
    """Check if a move is legal."""
    # need some way to check if a move would result in check
    raise NotImplemented

  def piece_at(self, location):
    """Get the piece at a given location or None if no piecei s found."""
    for piece in self.pieces:
      if piece.location == location:
        return piece
    return None

  def moves(self, player):
    """Get all the legal moves a player can make."""
    for piece in self.pieces:
      if piece.owner == player:
        for move in piece.moves:
          yield move

  def make_move(self, move):
    """Apply the given move to the board."""
    if self.is_legal(move):
      # TODO: Promotion
      for piece in self.pieces:
        if piece != move.piece and piece.location == move.to:
          self.pieces.remove(piece)
      move.piece.location = move.to
    else:
      raise ValueError("Illegal move.")
