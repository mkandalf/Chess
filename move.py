

class Move(object):
    def __init__(self, piece, to):
        self.to = to
        self.piece = piece

    def __eq__(self, other):
        return (self.piece == other.piece) and (self.to == other.to)

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "%s to %s" % (str(self.piece), self.to)

    def __repr__(self):
        return "%s to %s" % (repr(self.piece), self.to)
