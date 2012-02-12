

class Board(object):
    def __init__(self, pieces):
        self.pieces = pieces
        self.width = self.height = 8

    def in_check(self, player):
        """Check if the player is in check."""
        # TODO: implement
        return False

    def is_legal(self, move):
        """Check if a move is legal."""
        if move.piece.can_reach(self, move.to):
            # Need a good way to check if the move would result in check
            return True
        else:
            return False

    def moves(self, player):
        """Get all the moves a player can make."""
        for piece in self.pieces:
            if piece.owner == player:
                for move in piece.moves(self):
                    if self.is_legal(move):
                        yield move

    def stalemated(self, player):
        """Check if the given player is stalemated."""
        return len([_ for _ in self.moves(player)]) == 0 and \
                not self.in_check(player)

    def checkmated(self, player):
        """Check if the given player is checkmated."""
        return len([_ for _ in self.moves(player)]) == 0 and \
                self.in_check(player)

    def is_over(self, player):
        """Check if the game is over for the given player."""
        return self.checkmated(player) or self.stalemated(player)

    def piece_at(self, location):
        """Get the piece at a given location or None if no piecei s found."""
        for piece in self.pieces:
            if piece.location == location:
                return piece
        return None

    def make_move(self, move):
        """Apply the given move to the board."""
        if self.is_legal(move):
            # TODO: Promotion
            if self.piece_at(move.to):
                self.pieces.remove(self.piece_at(move.to))
            move.piece.location = move.to
        else:
            raise ValueError("Illegal move.")
