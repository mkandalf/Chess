from board import Board
from game import Game
from player import Player, Color 
from piece import Pawn, Bishop, Knight, Rook, Queen, King


if __name__ == "__main__":
  players = (Player(Color.WHITE), Player(Color.BLACK))
  pieces = set()
  for player in players:
    if player.color == Color.WHITE:
      for x in range(8):
        pieces.add(Pawn(player, (1, x)))
      pieces.add(Rook(player, (0, 0)))
      pieces.add(Knight(player, (0, 1)))
      pieces.add(Bishop(player, (0, 2)))
      pieces.add(Queen(player, (0, 3)))
      pieces.add(King(player, (0, 4)))
      pieces.add(Bishop(player, (0, 5)))
      pieces.add(Knight(player, (0, 6)))
      pieces.add(Rook(player, (0, 7)))
    else:
      for x in range(8):
        pieces.add(Pawn(player, (6, x)))
      pieces.add(Rook(player, (7, 0)))
      pieces.add(Knight(player, (7, 1)))
      pieces.add(Bishop(player, (7, 2)))
      pieces.add(Queen(player, (7, 3)))
      pieces.add(King(player, (7, 4)))
      pieces.add(Bishop(player, (7, 5)))
      pieces.add(Knight(player, (7, 6)))
      pieces.add(Rook(player, (7, 7)))
  board = Board(pieces)
  game = Game(board, players)
  game.play()
