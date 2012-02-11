from move import Move
from piece import Piece


class Pawn(Piece):
  @property
  def moves(self):
    if self.owner.color == "White":
      front_square = (self.x, self.y + 1)
      front_piece = self._board.piece_at(front_square)
      if front_piece is None:
        yield Move(self, front_square)

      diag_r = (self.x + 1, self.y + 1)
      diag_r_piece = self._board.piece_at(diag_r)
      if diag_r_piece is None:
        yield Move(self, diag_r)
