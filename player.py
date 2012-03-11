import random

from color import Color
from piece import Knight, Bishop, Rook, Queen, Pawn, King

from move_parser import MoveParser


class Player(object):
    def __init__(self, color):
        self.color = color
        self.castling = [(True, True)]

    @property
    def can_castle_queenside(self):
        return self.castling[-1][0]

    @property
    def can_castle_kingside(self):
        return self.castling[-1][1]

    def pieces(self, board):
        """Get all pieces owned by the player."""
        for piece in board.pieces:
            if piece.owner == self:
                yield piece

    def king(self, board):
        for piece in self.pieces(board):
            if type(piece) == King:
                return piece
        assert False, self.pieces(board)
    
    def moves(self, board):
        """Get all the moves a player can make."""
        for piece in self.pieces(board):
            for move in piece.moves(board):
                yield move

    def is_in_check(self, board):
        """Check if the player is in check.
        A player is in check if any piece owned by an opponent
        can reach the player's King."""
        return any(piece.can_attack(board, self.king(board).location)
                for piece in board.pieces if piece.owner != self)

    def get_move(self, board):
        """Request a valid move from the player."""
        return NotImplemented

    def __str__(self):
        return "White" if self.color == Color.WHITE else "Black"

    def __eq__(self, other):
        return self.color == other.color

    def __ne__(self, other):
        return not self == other

class CPU(Player):
    def get_move(self, board):
        """Request a valid move from the player."""
        return random.choice(list(self.moves(board)))

class Human(Player):
    def __init__(self, color):
        super(Human, self).__init__(color)
        self._move_parser = MoveParser()

    def get_move(self, board):
        """Request a valid move from the player."""
        while True:
            try:
                move = self._move_parser.parse_move(\
                        raw_input("Please enter your move: "), board)
            except ValueError as e:
                print e
            else:
                if move.piece is None:
                    print "No piece found."
                elif move.piece.owner != self:
                    print "You do not own that piece."
                else:
                    return move
