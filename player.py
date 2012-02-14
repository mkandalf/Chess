import re

from color import Color
from move import Move
from piece import Knight, Bishop, Rook, Queen, Pawn


class Player(object):
    def __init__(self, color):
        self.color = color
        self.castling = [(True, True)]

    _SQUARE_LOOKUP = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
            'e': 4, 'f': 5, 'g': 6, 'h': 7}

    def _parse_square(self, square):
        """Convert a square into a tuple."""
        assert len(square) == 2, len(square)
        f, r = square
        assert f in self._SQUARE_LOOKUP, f
        return self._SQUARE_LOOKUP[f], int(r) - 1

    def _parse_move(self, string, board):
        """Try to convert a string to move.
        Raises a ValueError if no move can be decoded."""
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
                return Move(piece, board.piece_at(to), \
                        start, to, promotion)

    def get_move(self, board):
        """Request a valid move from the player."""
        while True:
            try:
                move = self._parse_move(\
                        raw_input("Please enter your move: "), board)
            except ValueError as e:
                print e
            else:
                if move.piece is None:
                    print "No piece found."
                elif move.piece.owner != self:
                    print "You do not own that piece."
                elif not board.is_legal(move):
                    print "Illegal move"
                else:
                    return move

    def __str__(self):
        return "White" if self.color == Color.WHITE else "Black"

    def __eq__(self, other):
        return self.color == other.color

    def __ne__(self, other):
        return not self == other
