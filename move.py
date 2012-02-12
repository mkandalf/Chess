

class Move(object):
    def __init__(self, piece, captured, start, to):
        self.to = to
        self.start = start
        self.piece = piece
        self.captured = captured

    def __eq__(self, other):
        return ((self.piece == other.piece) 
                and (self.to == other.to)
                and (self.start == other.start) 
                and (self.captured == other.captured))

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "%s to %s from %s" % (str(self.piece), self.to, self.start)

    def __repr__(self):
        return "%s to %s from %s" % (repr(self.piece), self.to, self.start)
