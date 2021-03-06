import sys

from board import Board
from color import Color
from game import Game
from piece import Pawn, Bishop, Knight, Rook, Queen, King
from player import Human, CPU

def main():
    players = white, black = (CPU(Color.WHITE), Human(Color.BLACK))
    white.opponent, black.opponent = black, white
    board = Board()
    for player in players:
        if player.color == Color.WHITE:
            pawn_rank = 1
            piece_rank = 0
        else:
            pawn_rank = 6
            piece_rank = 7
        for x in range(8):
            board.add_piece(Pawn(player, (x, pawn_rank)))
        board.add_piece(Rook(player, (0, piece_rank)))
        board.add_piece(Knight(player, (1, piece_rank)))
        board.add_piece(Bishop(player, (2, piece_rank)))
        board.add_piece(Queen(player, (3, piece_rank)))
        board.add_piece(King(player, (4, piece_rank)))
        board.add_piece(Bishop(player, (5, piece_rank)))
        board.add_piece(Knight(player, (6, piece_rank)))
        board.add_piece(Rook(player, (7, piece_rank)))
    game = Game(board, players)
    game.play()
    return 0


if __name__ == "__main__":
    sys.exit(main())
