# import pprint

from color import Color
from piece import Knight, Bishop, Rook, Queen, Pawn, King

from move_parser import MoveParser
from position import Position


class Player(object):
    def __init__(self, color):
        self.color = color
        self.castling = [(True, True)]
        self.opponent = None  # must be set after init
        self.pieces = set()

    @property
    def can_castle_queenside(self):
        return self.castling[-1][0]

    @property
    def can_castle_kingside(self):
        return self.castling[-1][1]

    @property
    def king(self):
        for piece in self.pieces:
            if type(piece) == King:
                return piece

    def moves(self, board):
        """Get all the moves a player can make."""
        for piece in self.pieces:
            for move in piece.moves(board):
                yield move

    def is_in_check(self, board):
        """Check if the player is in check.
        A player is in check if any piece owned by an opponent
        can reach the player's King."""
        return any(piece.can_attack(board, self.king.location)
                for piece in self.opponent.pieces)

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
                score[move] = self._alphabeta(game, p, self.DEPTH, self)
        # pprint.pprint(score)

        # for some reason, max(score.keys, score.get) doesn't work.
        best_k, best_v = None, float("-inf")
        for k, v in score.items():
            if v > best_v:
                best_k = k
                best_v = v
        return best_k

    def _alphabeta(self, game, board, depth, player, a=float("-inf"), b=float("inf")):
        """Evaluate the fitness of a position."""
        # TODO: ref to game
        if depth == 0:
            return self._score(board)
        else:
            if player == self:
                for move in player.moves(board):
                    with Position(game, move) as p:
                        a = max(a, self._alphabeta(game, p, depth - 1, player.opponent, a, b))
                        if b <= a:
                            break
                return a
            else:
                for move in player.moves(board):
                    with Position(game, move) as p:
                        b = min(b, self._alphabeta(game, p, depth - 1, player.opponent, a, b))
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
                score += sum(1 for _ in piece.moves(board))
            else:
                score -= self.RELATIVE_VALUE[type(piece)]
                score -= sum(1 for _ in piece.moves(board))
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
