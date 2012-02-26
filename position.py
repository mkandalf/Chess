

class Position(object):
    def __init__(self, board, move):
        self.board = board
        self.move = move

    def __enter__(self):
        self.board.make_move(self.move)
        return self.board

    def __exit__(self, type, value, traceback):
        self.board.undo_move(self.move)
