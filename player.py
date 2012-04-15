import pprint
import random

from color import Color
from piece import Knight, Bishop, Rook, Queen, Pawn, King

from move_parser import MoveParser
from position import Position


class Player(object):
    def __init__(self, color):
        self.color = color
        self.castling = [(True, True)]
        self.opponent = None # must be set after init

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
    DEPTH = 2

    def get_move(self, game):
        """Request a valid move from the player."""
        score = {}
        for move in self.moves(game.board):
            with Position(game, move) as p:
                score[move] = self._alphabeta(game, p, self.DEPTH, float("-inf"), float("inf"), self)
        pprint.pprint(score)
        return max(score.keys(), key=lambda key: score[key])


    def _alphabeta(self, game, board, depth, a, b, player):
        """Evaluate the fitness of a position."""
        # TODO: ref to game
        if depth == 0:
            return self._score(board)
        else:
            if player == self:
                for move in player.moves(board):
                    with Position(game, move) as p:
                        a = max(a, self._alphabeta(game, p, depth - 1, a, b, player.opponent))
                        if b <= a:
                            break
                return a
            else:
                for move in player.moves(board):
                    with Position(game, move) as p:
                        b = min(b, self._alphabeta(game, p, depth - 1, a, b, player.opponent))
                        if b <= a:
                            break
                return b

    RELATIVE_VALUE = {
            Pawn: 1,
            Knight: 3,
            Bishop: 3,
            Rook: 5,
            Queen: 9,
            King: 0
            }
    
    def _score(self, board):
        """Evaluate the static fitness of a position."""
        score = 0
        for piece in board.pieces:
            if piece.owner == self:
                score += self.RELATIVE_VALUE[type(piece)]
                score += len(list(piece.moves(board)))
            else:
                score -= self.RELATIVE_VALUE[type(piece)]
                score -= len(list(piece.moves(board)))
        return score


class Human(Player):
    def __init__(self, color):
        super(Human, self).__init__(color)
        self._move_parser = MoveParser()

    def get_move(self, game):
        """Request a valid move from the player."""
        board = game.board
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
                elif not move.piece.can_reach(board, move.to):
                    print "Not a valid move."
                else:
                    return move
