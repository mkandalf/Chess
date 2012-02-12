from piece import King


class Board(object):
    def __init__(self, pieces = set()):
        self.pieces = pieces
        self.width = self.height = 8


    def __str__(self):
        a = [[" " for i in xrange(8)] for x in xrange(8)]
        divide = "+ - + - + - + - + - + - + - + - +"
        for piece in self.pieces:
            piece_str = str(piece)[0]
            if str(piece) == "Knight":
                piece_str = "N"
            if piece.owner != self.players[0]:
                piece_str = piece_str.lower()
            a[piece.location[1]][piece.location[0]] = piece_str
        for row in a:
            print divide
            for sq in row:
                if sq:
                    print "|", sq,
            print "|"
        print divide

    def on_board(self, loc):
        """Check if a location is on the board."""
        x, y = loc
        return 0 <= x < self.width and 0 <= y < self.height

    def in_check(self, player):
        """Check if the player is in check."""
        king = None
        for piece in self.pieces:
            if piece.owner == player:
                if type(piece) == King:
                    king = piece
                    break
        assert king is not None
        for piece in self.pieces:
            if piece.owner != player:
                for square in piece.reachable(self):
                    if square == king.location:
                        return True
        return False

    def make_move(self, move):
        """Apply the given move to the board."""
        # TODO: Promotion, castling
        if self.piece_at(move.to):
            self.pieces.remove(self.piece_at(move.to))
        move.piece.location = move.to

    def undo_move(self, move):
        """Apply the move in reverse to the board."""
        move.piece.location = move.start
        if move.captured is not None:
            self.pieces.add(move.captured)

    def is_legal(self, move):
        """Check if a move is legal."""
        if move.piece.can_reach(self, move.to):
            self.make_move(move)
            in_check = self.in_check(move.piece.owner)
            self.undo_move(move)
            return not in_check
        else:
            return False

    def moves(self, player):
        """Get all the legal moves a player can make."""
        for piece in self.pieces:
            if piece.owner == player:
                for move in piece.moves(self):
                    if self.is_legal(move):
                        yield move

    def is_over(self, player):
        """Check if the game is over for the given player."""
        return len(list(self.moves(player))) == 0

    def is_stalemate(self, player):
        """Check if the given player is stalemated."""
        return self.is_over(player) and not self.in_check(player)

    def is_checkmate(self, player):
        """Check if the given player is checkmated."""
        return self.is_over(player) and self.in_check(player)

    def piece_at(self, location):
        """Get the piece at a given location or None if no piece is found."""
        for piece in self.pieces:
            if piece.location == location:
                return piece
        return None
