from piece import Pawn, Bishop, Knight, Rook, Queen, King
from player import Player, Color
from position import Position


class Game(object):
    def __init__(self, board,
            players=(Player(Color.WHITE), Player(Color.BLACK))):
        self.ply = 0
        self.board = board
        self.players = players

    @property
    def current_player(self):
        """The player whose turn it is."""
        return self.players[self.ply % 2]

    def is_legal(self, move):
        """Check if a move is legal.
        A move is legal if
        * a piece can reach the target square
        * an allied piece is not on the target square
        * moving would not place the owner in check."""
        if move.piece.can_reach(self.board, move.to):
            piece = self.board.piece_at(move.to)
            if piece is None or piece.owner != move.piece.owner:
                # disallow castling through check
                if type(move.piece) == King:
                    dx = move.to[0] - move.start[0]
                    if abs(dx) == 2:  # castle
                        through = move.start[0] + dx / 2, move.to[1]
                        if any(piece.can_attack(self.board, through)
                                for piece in self.board.pieces
                                if piece.owner != move.piece.owner):
                            return False

                with Position(self.board, move) as position:
                    return not move.piece.owner.is_in_check(position)
            else:
                return False
        else:
            return False

    @property
    def is_over(self):
        """Check if the game is over for the given player.
        The game is over if a player cannot make any moves."""
        return not any(self.is_legal(move)
                for move in self.current_player.moves(self.board))

    def is_checkmate(self, player):
        """Check if the given player is checkmated.
        A player is checkmated if the game is over
        and the player is in check."""
        return self.is_over and player.is_in_check(self.board)

    def is_stalemate(self, player):
        """Check if the given player is stalemated.
        A player is stalemated if the game is over
        and the player is not in check."""
        return self.is_over and not player.is_in_check(self.board)

    def from_fen(self, fen):
        """Reset game to match given FEN string"""
        self.board.pieces = set()
        components = fen.split(" ")
        rows = components[0].split("/")
        for row, row_str in enumerate(rows):
            column = 0
            for entry in row_str:
                if entry.isdigit():
                    column += int(entry)
                else:
                    sq = (column, 7 - row)
                    player = self.players[not entry.islower()]
                    entry = entry.lower()
                    if entry.lower() == "r":
                        self.board.pieces.add(Rook(player, sq))
                    elif entry.lower() == "n":
                        self.board.pieces.add(Knight(player, sq))
                    elif entry.lower() == "b":
                        self.board.pieces.add(Bishop(player, sq))
                    elif entry.lower() == "q":
                        self.board.pieces.add(Queen(player, sq))
                    elif entry.lower() == "k":
                        self.board.pieces.add(King(player, sq))
                    elif entry.lower() == "p":
                        self.board.pieces.add(Pawn(player, sq))
                    column += 1
        self.ply = int(components[1] == "b") + int(components[5]) - 1

    def play(self):
        """Play the game."""
        print "Starting game."
        print "Press CTRL+C to quit."
        print self.board
        while not self.is_over:
            print "%s's turn." % self.current_player
            move = self.current_player.get_move(self.board)
            print move
            if self.is_legal(move):
                self.board.make_move(move)
                self.ply += 1
                print self.board
            else:
                print "Illegal move."
        if self.is_checkmate(self.current_player):
            print "Checkmate."
        else:
            print "Stalemate"
        print "Game over."
