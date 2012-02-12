import re

from move import Move


class Color(object):
    WHITE = 0
    BLACK = 1


class Player(object):
    def __init__(self, color):
        self.color = color

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
        matches = re.search("([a-h][1-8]).*([a-h][1-8])", string)
        if matches is not None:
            start, end = matches.groups()
            start_sq = self._parse_square(start)
            piece = board.piece_at(start_sq)
            to = self._parse_square(end)
            return Move(piece, board.piece_at(to), to, start_sq)
        else:
            raise ValueError("Could not parse input. Try again.")

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
