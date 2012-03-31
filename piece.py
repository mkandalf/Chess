from itertools import product

from color import Color
from move import Move


class Piece(object):
    """Abstract base class for pieces."""
    def __init__(self, owner, location):
        self.owner = owner
        self._location = location

    @property
    def location(self):
        return self._location

    @property
    def x(self):
        return self._location[0]

    @property
    def y(self):
        return self._location[1]

    def attackable(self, board):
        """Get all the squares this piece can attack."""
        raise NotImplemented

    def can_attack(self, board, square):
        """Check if the given square can be attacked."""
        return any(attack == square for attack in self.attackable(board))

    def moves(self, board):
        for square in self.attackable(board):
            piece = board.piece_at(square)
            move = Move(self, self.location, square, piece)
            yield move

    def reachable(self, board):
        """Get all the squares this pice can reach."""
        for move in self.moves(board):
            yield move.to

    def can_reach(self, board, square):
        """Check if the given square is reachable."""
        return square in self.reachable(board)

    def __eq__(self, other):
        return self.owner == other.owner and self.location == other.location

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "%s %s %s" % (self.owner.color, str(self), self.location)


class VectorPiece(Piece):
    """A piece that attacks along vectors."""
    _vectors = []

    def attackable(self, board):
        for vector in self._vectors:
            u, v = vector
            x, y = self.x + u, self.y + v
            while board.is_on_board((x, y)):
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


class Bishop(VectorPiece):
    _vectors = ((1, 1), (-1, 1), (-1, -1), (1, -1))

    def __str__(self):
        return "Bishop"


class Rook(VectorPiece):
    _vectors = ((1, 0), (0, 1), (-1, 0), (0, -1))

    def __str__(self):
        return "Rook"


class Queen(VectorPiece):
    _vectors = ((1, 0), (0, 1), (-1, 0), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1))

    def __str__(self):
        return "Queen"


class Knight(Piece):
    _vectors = ((1, 2), (1, -2), (-1, 2), (-1, -2),
            (2, 1), (2, -1), (-2, 1), (-2, -1))

    def attackable(self, board):
        for vector in self._vectors:
            x, y = vector
            square = self.x + x, self.y + y
            if board.is_on_board(square):
                piece = board.piece_at(square)
                if piece is None or piece.owner != self.owner:
                    yield square

    def __str__(self):
        return "Knight"


class King(Piece):
    def attackable(self, board):
        for x, y in product(range(-1, 2), range(-1, 2)):
            if not (x == y == 0):
                square = (self.x + x, self.y + y)
                if board.is_on_board(square):
                    piece = board.piece_at(square)
                    if piece is None or piece.owner != self.owner:
                        yield square

    def moves(self, board):
        """Get all the possible moves for the piece.
        Moves are guaranteed to be reachable, but not legal."""
        for move in super(King, self).moves(board):
            yield move

        #Castling moves aren't necessarily legal
        if not self.owner.is_in_check(board):
            if self.owner.can_castle_queenside:
                left1 = board.piece_at((self.x - 1, self.y))
                left2 = board.piece_at((self.x - 2, self.y))
                if left1 is None and left2 is None:
                    yield Move(self, self.location, (self.x - 2, self.y))
            if self.owner.can_castle_kingside:
                if (board.piece_at((self.x + 1, self.y)) is None
                    and board.piece_at((self.x + 2, self.y)) is None):
                    yield Move(self, self.location, (self.x + 2, self.y))

    def __str__(self):
        return "King"


class Pawn(Piece):
    promotable = (Knight, Bishop, Rook, Queen)

    def __init__(self, owner, location, just_moved=False):
        super(Pawn, self).__init__(owner, location)
        self.just_moved = just_moved

    @property
    def promotion_rank(self):
        return 7 if self.owner.color == Color.WHITE else 0

    @property
    def start_rank(self):
        return 1 if self.owner.color == Color.WHITE else 6

    @property
    def _vector(self):
        return 1 if self.owner.color == Color.WHITE else -1

    def attackable(self, board):
        for dx in (-1, 1):
            square = self.x + dx, self.y + self._vector
            piece = board.piece_at(square)
            if piece is not None and piece.owner != self.owner:
                yield square

    def moves(self, board):
        for square in self.attackable(board):
            piece = board.piece_at(square)
            if square[1] == self.promotion_rank:
                for promote in self.promotable:
                    move = Move(self, self.location, square, \
                            piece, promote)
                    yield move
            else:
                yield Move(self, self.location, square, piece)

        # en passant
        for dx in (-1, 1):
            square = self.x + dx, self.y
            piece = board.piece_at(square)
            if type(piece) == Pawn and piece.just_moved:
                if piece.owner != self.owner:
                    yield Move(self, self.location, square, piece)

        # forward
        square = self.x, self.y + self._vector
        if not board.piece_at(square):
            if square[1] == self.promotion_rank:
                for promote in self.promotable:
                    yield Move(self, self.location, square, None, promote)
            else:
                yield Move(self, self.location, square)

        # forward2
            if self.y == self.start_rank:
                square = self.x, self.y + self._vector * 2
                if not board.piece_at(square):
                    yield Move(self, self.location, square)

    def __str__(self):
        return "Pawn"
