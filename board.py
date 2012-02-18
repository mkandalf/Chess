from piece import King, Pawn, Rook
from color import Color


class Board(object):
    def __init__(self, pieces=None):
        self.pieces = pieces or set()
        self.width = self.height = 8

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
            if piece.owner != player and type(piece) != King:
                for move in piece.moves(self):
                    if move.to == king.location:
                        return True
        return False

    def make_move(self, move):
        """Apply the given move to the board."""
        #Handle castling
        if type(move.piece) == King:
            dy = move.to[0] - move.start[0]
            if abs(dy) == 2:
                if dy == 2:
                    rook = self.piece_at((7, move.to[1]))
                    rook.location = (5, move.to[1])
                else:
                    rook = self.piece_at((0, move.to[1]))
                    rook.location = (3, move.to[1])
            move.piece.owner.castling.append((False, False))
        #Remove castling rights on rook moves
        elif type(move.piece) == Rook:
            if move.start[0] == 0:
                move.piece.owner.castling.append(
                        (False, move.piece.owner.castling[-1][1]))
            if move.start[0] == 7:
                move.piece.owner.castling.append(
                        (move.piece.owner.castling[-1][0], False))
            else:
                move.piece.owner.castling.append(move.piece.owner.castling[-1])
        #Otherwise repeat the last set of castling rights
        else:
            move.piece.owner.castling.append(move.piece.owner.castling[-1])

        if type(move.piece) == Pawn:
            pawn = move.piece
            pawn.just_moved = (pawn.y == pawn.start_rank)

        if move.captured is not None:
            self.pieces.remove(move.captured)
        move.piece.location = move.to

        if move.promotion is not None:
            promoted = move.promotion(move.piece.owner, move.piece.location)
            self.pieces.remove(move.piece)
            self.pieces.add(promoted)

    def undo_move(self, move):
        """Apply the move in reverse to the board."""
        move.piece.owner.castling.pop()
        if type(move.piece) == King:
            dy = move.to[0] - move.start[0]
            if dy == 2:
                rook = self.piece_at((5, move.to[1]))
                rook.location = (7, move.to[1])
                print rook.location
            elif dy == -2:
                rook = self.piece_at((3, move.to[1]))
                rook.location = (0, move.to[1])
        move.piece.location = move.start
        if move.captured is not None:
            self.pieces.add(move.captured)
        if move.promotion is not None:
            pawn = Pawn(move.piece.owner, move.piece.location)
            promoted = move.promotion(move.piece.owner, move.piece.location)
            for piece in self.pieces:
                if piece == promoted:
                    break
            self.pieces.remove(piece)
            self.pieces.add(pawn)

    def is_legal(self, move):
        """Check if a move is legal."""
        if move.piece.can_reach(self, move.to):
            if type(move.piece) == King:
                if abs(move.to[0] - move.start[0]) == 2:
                    if not self._is_castle_legal(move):
                        return False
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

    def _is_castle_legal(self, move):
        """Check if castling move is legal"""
        for piece in self.pieces:
            if piece.owner != move.piece.owner:
                for move2 in piece.moves(self):
                    pass_through = (move.start[0]
                            + ((move.to[0] - move.start[0]) / 2),
                            move.to[1])
                    if move2.to == pass_through:
                        return False
        return True

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
