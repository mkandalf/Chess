

class Move(object):
    def __init__(self, piece, start, to, captured=None, promotion=None):
        self.piece = piece
        self.start = start
        self.to = to
        self.captured = captured
        self.promotion = promotion

    def __eq__(self, other):
        return ((self.piece == other.piece)
                and (self.to == other.to)
                and (self.start == other.start)
                and (self.captured == other.captured)
                and (self.promotion == other.promotion))

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "%s to %s from %s" % (str(self.piece), self.to, self.start)

    def __repr__(self):
        return "%s from %s to %s captures %s" \
                % (str(self.piece), self.start, self.to, self.captured)
