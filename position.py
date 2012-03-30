

class Position(object):
    def __init__(self, game, move):
        self.game = game
        self.move = move

    def __enter__(self):
        self.game._make_move(self.move)
        return self.game.board

    def __exit__(self, type, value, traceback):
        self.game._undo_move()
