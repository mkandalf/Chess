import re

from move import Move
from piece import Pawn, Queen, Knight, Bishop, Rook


class MoveParser(object):
    def _parse_square(self, square):
        """Convert a square into an x-y coordinate."""
        assert len(square) == 2
        f, r = square
        assert f in "abcdefgh"
        return "abcdefgh".index(f), int(r) - 1

    def parse_move(self, string, board):
        """Try to convert a string into a move.
        Raises a ValueError if no move can be parsed."""
        tokens = string.strip().split()
        if len(tokens) < 2:
            raise ValueError("Please enter two squares.")
        else:
            start_square = re.search("[a-h][1-8]", tokens[0])
            end_square = re.search("[a-h][1-8]", tokens[1])
            if start_square is None or end_square is None:
                raise ValueError("Could not parse squares. Try again.")
            else:
                start = self._parse_square(start_square.group(0))
                piece = board.piece_at(start)
                to = self._parse_square(end_square.group(0))
                promotion = None
                if len(tokens) == 3 and type(piece) == Pawn:
                    if tokens[2] in ("Queen", "Q"):
                        promotion = Queen
                    elif tokens[2] in ("Knight", "N"):
                        promotion = Knight
                    elif tokens[2] in ("Bishop", "B"):
                        promotion = Bishop
                    elif tokens[2] in ("Rook", "R"):
                        promotion = Rook
                    else:
                        raise ValueError("Could not parse promotion.")
                return Move(piece, start, to, board.piece_at(to), promotion)
