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
        pieces.add(Pawn(player, (x, 1)))
      pieces.add(Rook(player, (0, 0)))
      pieces.add(Knight(player, (1, 0)))
      pieces.add(Bishop(player, (2, 0)))
      pieces.add(Queen(player, (3, 0)))
      pieces.add(King(player, (4, 0)))
      pieces.add(Bishop(player, (5, 0)))
      pieces.add(Knight(player, (6, 0)))
      pieces.add(Rook(player, (7, 0)))
    else:
      for x in range(8):
        pieces.add(Pawn(player, (x, 6)))
      pieces.add(Rook(player, (0, 7)))
      pieces.add(Knight(player, (1, 7)))
      pieces.add(Bishop(player, (2, 7)))
      pieces.add(Queen(player, (3, 7)))
      pieces.add(King(player, (4, 7)))
      pieces.add(Bishop(player, (5, 7)))
      pieces.add(Knight(player, (6, 7)))
      pieces.add(Rook(player, (7, 7)))
  board = Board(pieces)
  game = Game(board, players)
  game.play()
