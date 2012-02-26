from position import Position


class Move(object):
    def __init__(self, piece, start, to, captured=None, promotion=None):
        self.piece = piece
        self.start = start
        self.to = to
        self.captured = captured
        self.promotion = promotion

    def is_legal(self, board):
        """Check if a move is legal.
        A move is legal if
        * a piece can reach the target square
        * an allied piece is not on the target square
        * moving would not place the owner in check."""
        if self.piece.can_reach(board, self.to):
            piece = board.piece_at(self.to)
            if piece is None or piece.owner != self.piece.owner:
                with Position(board, self) as position:
                    return not position.in_check(self.piece.owner)
            else:
                return False
        else:
            return False

    def __eq__(self, other):
        return ((self.piece == other.piece)
                and (self.to == other.to)
                and (self.start == other.start)
                and (self.captured == other.captured)
                and (self.promotion == other.promotion))

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "%s from %s to %s captures %s" \
                % (str(self.piece), self.start, self.to, self.captured)

    def __repr__(self):
        if self.captured:
            return "%s from %s to %s captures %s" \
                % (str(self.piece), self.start, self.to, self.captured)
        else:
            return "%s from %s to %s" \
                % (str(self.piece), self.start, self.to)
