from color import Color


class Board(object):
    def __init__(self, pieces=None):
        self._pieces = pieces or {}
        assert type(self._pieces) == dict

    @property
    def width(self):
        return 8

    @property
    def height(self):
        return 8

    @property
    def pieces(self):
        return set(self._pieces.values())

    LOCS = {}

    def is_on_board(self, loc):
        """Check if a location is on the board."""
        try:
            return self.LOCS[loc]
        except KeyError:
            x, y = loc
            self.LOCS[loc] = result = 0 <= x < self.width and 0 <= y < self.height
            return result


    def piece_at(self, location):
        """Get the piece at a given location or None if no piece is found."""
        return self._pieces.get(location, None)

    def add_piece(self, piece):
        """Add a piece to the board."""
        assert self.piece_at(piece.location) is None
        self._pieces[piece.location] = piece
        piece.owner.pieces.add(piece)

    def move_piece(self, piece, loc):
        """Move a piece to the specified square."""
        self.remove_piece(piece)
        piece._location = loc
        self.add_piece(piece)

    def remove_piece(self, piece):
        """Remove a piece from the board."""
        assert self.piece_at(piece.location) == piece
        piece.owner.pieces.remove(piece)
        del self._pieces[piece.location]

    def __eq__(self, other):
        return self._pieces == other._pieces

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
