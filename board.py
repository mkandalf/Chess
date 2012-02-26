from piece import King, Pawn, Rook
from color import Color


class Board(object):
    def __init__(self, pieces=None):
        self.pieces = pieces or set()

    @property
    def width(self):
        return 8

    @property
    def height(self):
        return 8

    def is_on_board(self, loc):
        """Check if a location is on the board."""
        x, y = loc
        return 0 <= x < self.width and 0 <= y < self.height

    def piece_at(self, location):
        """Get the piece at a given location or None if no piece is found."""
        for piece in self.pieces:
            if piece.location == location:
                return piece
        return None

    def is_ally_at(self, location, player):
        piece = self.piece_at(location)
        if piece is None:
            return False
        else:
            return (piece.owner == player)

    def make_move(self, move):
        """Apply the given move to the board."""
        #Handle castling
        if type(move.piece) == King:
            dy = move.to[0] - move.start[0]
            if abs(dy) == 2:
                if dy == 2:
                    rook = self.piece_at((7, move.to[1]))
                    assert rook is not None, (move.piece, self.pieces)
                    rook.location = (5, move.to[1])
                else:
                    rook = self.piece_at((0, move.to[1]))
                    assert rook is not None, (move.piece, self.pieces)
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
            assert move.captured in self.pieces, (move.captured, self.pieces)
            self.pieces.remove(move.captured)
        move.piece.location = move.to

        if move.promotion is not None:
            promoted = move.promotion(move.piece.owner, move.piece.location)
            assert move.piece in self.pieces, (move.piece, self.pieces)
            self.pieces.remove(move.piece)
            self.pieces.add(promoted)

    def undo_move(self, move):
        """Apply the move in reverse to the board."""
        # restore castling rights
        move.piece.owner.castling.pop()

        # if move was a castle, restore rook position
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

    def __eq__(self, other):
        return self.pieces == other.pieces

    def __ne__(self, other):
        return not (self == other)

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
