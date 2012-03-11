from board import Board
from color import Color
from game import Game
from piece import Pawn, Bishop, Knight, Rook, Queen, King
from player import Human, CPU


if __name__ == "__main__":
    players = (CPU(Color.WHITE), Human(Color.BLACK))
    pieces = set()
    for player in players:
        if player.color == Color.WHITE:
            pawn_rank = 1
            piece_rank = 0
        else:
            pawn_rank = 6
            piece_rank = 7
        for x in range(8):
            pieces.add(Pawn(player, (x, pawn_rank)))
        pieces.add(Rook(player, (0, piece_rank)))
        pieces.add(Knight(player, (1, piece_rank)))
        pieces.add(Bishop(player, (2, piece_rank)))
        pieces.add(Queen(player, (3, piece_rank)))
        pieces.add(King(player, (4, piece_rank)))
        pieces.add(Bishop(player, (5, piece_rank)))
        pieces.add(Knight(player, (6, piece_rank)))
        pieces.add(Rook(player, (7, piece_rank)))
    board = Board(pieces)
    game = Game(board, players)
    game.play()
