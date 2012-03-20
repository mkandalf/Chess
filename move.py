from collections import namedtuple


class Move(namedtuple('Move', 'piece start to captured promotion')):
    def __new__(cls, piece, start, to, captured=None, promotion=None):
        # add default values
        return super(Move, cls).__new__(cls, piece, start, to, captured, promotion)

    def __str__(self):
        return "%s from %s to %s captures %s" \
                % (str(self.piece), self.start, self.to, self.captured)
