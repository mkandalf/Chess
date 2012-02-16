from player import Player, Color
from piece import Pawn, Bishop, Knight, Rook, Queen, King

class Game(object):
    def __init__(self, board, players=(Player(Color.BLACK), Player(Color.WHITE))):
        self.ply = 0
        self.board = board
        self.players = players

    @property
    def _current_player(self):
        """The player whose turn it is."""
        return self.players[self.ply % 2]

    def is_over(self, player):
        """Check if the game is over."""
        return self.board.is_over(player)

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
        while not self.is_over(self._current_player):
            print "%s's turn." % self._current_player
            move = self._current_player.get_move(self.board)
            print move
            self.board.make_move(move)
            self.ply += 1
            print self.board 
        if self.board.is_checkmate(self._current_player):
            print "Checkmate."
        else:
            print "Stalemate"
        print "Game over."
