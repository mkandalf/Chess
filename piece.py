from itertools import product

from player import Color
from move import Move


class Piece(object):
    """Abstract base class for pieces."""
    def __init__(self, owner, location):
        self.owner = owner
        self.location = location

    @property
    def location(self):
        return self.x, self.y

    @location.setter
    def location(self, value):
        self.x, self.y = value

    def reachable(self, board):
        """Get all the square reachable from the piece's current location.
        Reachable moves are guarantted to be on the board,
        but not guaranteed to be legal."""
        raise NotImplemented

    def moves(self, board):
        """Get all the possible moves for the piece.
        Moves are guaranteed to be reachable, but not legal."""
        for square in self.reachable(board):
            yield Move(self, board.piece_at(square), (self.x, self.y), square)

    def can_reach(self, board, square):
        """Check if the given square is reachable."""
        return any(s == square for s in self.reachable(board))

    def __eq__(self, other):
        return self.owner == other.owner and self.location == other.location

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "%s %s" % (str(self), self.location)


class Knight(Piece):
    _vectors = ((1, 2), (1, -2), (-1, 2), (-1, -2),
            (2, 1), (2, -1), (-2, 1), (-2, -1))

    def reachable(self, board):
        for vector in self._vectors:
            x, y = vector
            new_loc = self.x + x, self.y + y
            if board.on_board(new_loc):
                piece = board.piece_at(new_loc)
                if piece is None or piece.owner != self.owner:
                    yield new_loc

    def __str__(self):
        return "Knight"


class Bishop(Piece):
    _vectors = ((1, 1), (-1, 1), (-1, -1), (1, -1))

    def reachable(self, board):
        for vector in self._vectors:
            u, v = vector
            x, y = self.x + u, self.y + v
            while board.on_board((x, y)):
                loc = (x, y)
                piece = board.piece_at(loc)
                if piece is None:
                    yield loc
                else:
                    if piece.owner != self.owner:
                        yield loc
                    break
                x += u
                y += v

    def __str__(self):
        return "Bishop"


class Rook(Piece):
    _vectors = ((1, 0), (0, 1), (-1, 0), (0, -1))

    def reachable(self, board):
        for vector in self._vectors:
            u, v = vector
            x, y = self.x + u, self.y + v
            while board.on_board((x, y)):
                loc = (x, y)
                piece = board.piece_at(loc)
                if piece is None:
                    yield loc
                else:
                    if piece.owner != self.owner:
                        yield loc
                    break
                x += u
                y += v

    def __str__(self):
        return "Rook"


class King(Piece):
    def reachable(self, board):
        for x, y in product(range(-1, 2), range(-1, 2)):
            if not (x == y == 0):
                to = (self.x + x, self.y + y)
                if board.on_board(to):
                    piece = board.piece_at(to)
                    if piece is None or piece.owner != self.owner:
                        yield to

    def __str__(self):
        return "King"


class Queen(Piece):
    _vectors = ((1, 0), (0, 1), (-1, 0), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1))

    def reachable(self, board):
        for vector in self._vectors:
            u, v = vector
            x, y = self.x + u, self.y + v
            while board.on_board((x, y)):
                loc = (x, y)
                piece = board.piece_at(loc)
                if piece is None:
                    yield loc
                else:
                    if piece.owner != self.owner:
                        yield loc
                    break
                x += u
                y += v

    def __str__(self):
        return "Queen"


class Pawn(Piece):
    promotable = (Knight, Bishop, Rook, Queen)

    @property
    def promotion_rank(self):
        return 7 if self.owner.color == Color.WHITE else 0

    def moves(self, board):
        """Get all the possible moves for the piece.
        Moves are guaranteed to be reachable, but not legal."""
        for square in self.reachable(board):
            if square[1] == self.promotion_rank:
                for piece in self.promotable:
                    yield Move(self, board.piece_at(square), \
                            self.location, square, piece)
            else:
                yield Move(self, board.piece_at(square), \
                        self.location, square)

    @property
    def start_rank(self):
        return 1 if self.owner.color == Color.WHITE else 6

    @property
    def _vector(self):
        return 1 if self.owner.color == Color.WHITE else -1

    def reachable(self, board):
        forward_1 = self.x, self.y + self._vector
        if not board.piece_at(forward_1):
            yield forward_1
            if self.y == self.start_rank:
                forward_2 = self.x, self.y + self._vector * 2
                if not board.piece_at(forward_2):
                    yield forward_2
        attack1 = self.x - 1, self.y + self._vector
        piece = board.piece_at(attack1)
        if piece is not None and piece.owner != self.owner:
            yield attack1
        attack2 = self.x + 1, self.y + self._vector
        piece = board.piece_at(attack2)
        if piece is not None and piece.owner != self.owner:
            yield attack2

    def __str__(self):
        return "Pawn"
