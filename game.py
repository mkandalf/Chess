

class Game(object):
    def __init__(self, board, players):
        self.turn = 0
        self.board = board
        self.players = players

    @property
    def _current_player(self):
        """The player whose turn it is."""
        return self.players[self.turn % 2]

    def is_over(self, player):
        """Check if the game is over."""
        return self.board.is_over(player)

    def play(self):
        """Play the game."""
        print "Starting game."
        print "Press CTRL+C to quit."
        while not self.is_over(self._current_player):
            print "%s's turn." % self._current_player
            move = self._current_player.get_move(self.board)
            print "%s %s to %s" % (move.piece, move.piece.location, move.to)
            self.board.make_move(move)
            self.turn += 1
        print "Game over."
