from color import Color


class Board(object):
    def __init__(self, pieces=None):
        self.pieces = pieces or set()

    @property
    def width(self):
        return 8

    @property
    def height(self):
        return 8

    def is_on_board(self, loc):
        """Check if a location is on the board."""
        x, y = loc
        return 0 <= x < self.width and 0 <= y < self.height

    def piece_at(self, location):
        """Get the piece at a given location or None if no piece is found."""
        for piece in self.pieces:
            if piece.location == location:
                return piece
        return None

    def is_ally_at(self, location, player):
        piece = self.piece_at(location)
        if piece is None:
            return False
        else:
            return (piece.owner == player)

    def __eq__(self, other):
        return self.pieces == other.pieces

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        a = [[" " for i in xrange(8)] for x in xrange(8)]
        ret = ""
        divide = "+-+-+-+-+-+-+-+-+\n"
        for piece in self.pieces:
            piece_str = str(piece)[0]
            if str(piece) == "Knight":
                piece_str = "N"
            if piece.owner.color == Color.BLACK:
                piece_str = piece_str.lower()
            a[7 - piece.location[1]][piece.location[0]] = piece_str
        for row in a:
            ret += divide
            for sq in row:
                if sq:
                    ret += "|" + sq
            ret += "|\n"
        return ret + divide
