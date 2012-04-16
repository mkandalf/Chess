import unittest

from board import Board
from color import Color
from move import Move
from move_parser import MoveParser
from player import Player
from game import Game
from piece import King, Knight, Rook, Bishop, Queen, Pawn


class ChessTest(unittest.TestCase):
    def setUp(self):
        self.board = Board(dict())
        self.white = Player(Color.WHITE)
        self.black = Player(Color.BLACK)
        self.white.opponent, self.black.opponent = self.black, self.white
        self.game = Game(self.board, (self.white, self.black))


class PawnTest(ChessTest):
    def test_en_passant(self):
        pawn1 = Pawn(self.white, (4, 4))
        pawn2 = Pawn(self.black, (3, 6))
        self.board.add_piece(pawn1)
        self.board.add_piece(pawn2)
        move = Move(pawn2, pawn2.location, (3, 4))
        self.game._make_move(move)
        moves = [m for m in pawn1.moves(self.board)]
        self.assertEqual(len(moves), 2)

    def test_cant_en_passant(self):
        pawn1 = Pawn(self.white, (4, 4))
        pawn2 = Pawn(self.black, (3, 5))
        self.board.add_piece(pawn1)
        self.board.add_piece(pawn2)
        move = Move(pawn2, pawn2.location, (3, 4))
        self.game._make_move(move)
        moves = [m for m in pawn1.moves(self.board)]
        self.assertEqual(len(moves), 1)

    def test_bad_capture(self):
        self.white.castling.append((False, False))
        pawn1 = Pawn(self.white, (4, 1))
        pawn2 = Pawn(self.white, (5, 1))
        king1 = King(self.white, (4, 0))
        king2 = King(self.black, (4, 7))
        self.board.add_piece(pawn1)
        self.board.add_piece(pawn2)
        self.board.add_piece(king1)
        self.board.add_piece(king2)
        self.assertTrue(
                [move.captured is None
                    for move in self.white.moves(self.board)])

    def test_moves_center(self):
        pawn = Pawn(self.white, (4, 4))
        moves = list(pawn.moves(self.board))
        self.assertEquals(len(moves), 1, moves)

    def test_moves_start(self):
        pawn = Pawn(self.white, (4, 1))
        moves = list(pawn.moves(self.board))
        self.assertEquals(len(moves), 2, moves)

    def test_moves_start_blocked(self):
        pawn = Pawn(self.white, (4, 1))
        bishop = Bishop(self.white, (4, 3))
        self.board.add_piece(bishop)
        moves = list(pawn.moves(self.board))
        self.assertEquals(len(moves), 1, moves)

    def test_moves_blocked_ally(self):
        pawn = Pawn(self.white, (4, 4))
        bishop = Bishop(self.white, (4, 5))
        self.board.add_piece(bishop)
        moves = list(pawn.moves(self.board))
        self.assertEquals(len(moves), 0, moves)

    def test_moves_blocked_enemy(self):
        pawn = Pawn(self.white, (4, 4))
        bishop = Bishop(self.black, (4, 5))
        self.board.add_piece(bishop)
        moves = list(pawn.moves(self.board))
        self.assertEquals(len(moves), 0, moves)

    def test_moves_captureable_enemy(self):
        king = King(self.white, (0, 4))
        pawn = Pawn(self.white, (4, 4))
        bishop = Bishop(self.black, (5, 5))
        self.board.add_piece(king)
        self.board.add_piece(pawn)
        self.board.add_piece(bishop)
        moves = list(pawn.moves(self.board))
        self.assertEquals(len(moves), 2, moves)

    def test_promotions(self):
        pawn = Pawn(self.white, (4, 6))
        moves = list(pawn.moves(self.board))
        self.assertEquals(len(moves), 4, moves)

    def test_promotions_are_valid(self):
        pawn = Pawn(self.white, (4, 6))
        moves = list(pawn.moves(self.board))
        self.assertTrue(all(move.promotion is not None for move in moves))

    def test_promotions_with_capturable(self):
        pawn = Pawn(self.white, (4, 6))
        rook = Rook(self.black, (3, 7))
        self.board.add_piece(pawn)
        self.board.add_piece(rook)
        moves = list(pawn.moves(self.board))
        self.assertTrue(len(moves), 8)

    def test_promotions_are_valid_with_capturable(self):
        pawn = Pawn(self.white, (4, 6))
        rook = Rook(self.black, (3, 7))
        self.board.add_piece(pawn)
        self.board.add_piece(rook)
        moves = list(pawn.moves(self.board))
        self.assertTrue(all(move.promotion is not None for move in moves))


class KingTest(ChessTest):
    def test_castle(self):
        rook1 = Rook(self.white, (0, 0))
        king = King(self.white, (4, 0))
        rook2 = Rook(self.white, (7, 0))
        self.board.add_piece(king)
        self.board.add_piece(rook1)
        self.board.add_piece(rook2)
        moves = list(self.white.moves(self.board))
        self.assertEquals(len(moves), 26)

    def test_castle_through_check(self):
        rook1 = Rook(self.white, (0, 0))
        king = King(self.white, (4, 0))
        rook2 = Rook(self.white, (7, 0))
        knight = Knight(self.black, (2, 2))
        self.board.add_piece(king)
        self.board.add_piece(rook1)
        self.board.add_piece(rook2)
        self.board.add_piece(knight)
        move = Move(king, king.location, (2, 0))
        self.assertFalse(self.game.is_legal(move))

    def test_cant_castle_out_of_check(self):
        king = King(self.white, (4, 0))
        rook1 = Rook(self.white, (0, 0))
        rook2 = Rook(self.black, (4, 7))
        self.board.add_piece(king)
        self.board.add_piece(rook1)
        self.board.add_piece(rook2)
        move = Move(king, king.location, (2, 0))
        self.assertFalse(self.game.is_legal(move))

    def test_moves_center(self):
        self.white.castling.append((False, False))
        king = King(self.white, (4, 4))
        self.board.add_piece(king)
        moves = list(king.moves(self.board))
        self.assertEquals(len(moves), 8, moves)

    def test_moves_blocked_ally(self):
        self.white.castling.append((False, False))
        king = King(self.white, (4, 4))
        knight = Knight(self.white, (3, 3))
        self.board.add_piece(king)
        self.board.add_piece(knight)
        moves = list(king.moves(self.board))
        self.assertEquals(len(moves), 7, moves)

    def test_moves_blocked_enemy(self):
        self.white.castling.append((False, False))
        king = King(self.white, (4, 4))
        knight = Knight(self.black, (3, 3))
        self.board.add_piece(king)
        self.board.add_piece(knight)
        moves = list(king.moves(self.board))
        self.assertEquals(len(moves), 8, moves)

    def test_moves_corner(self):
        self.white.castling.append((False, False))
        king = King(self.white, (0, 0))
        self.board.add_piece(king)
        moves = list(king.moves(self.board))
        self.assertEquals(len(moves), 3, moves)

    def test_can_reach_normal(self):
        king = King(self.white, (4, 4))
        self.board.add_piece(king)
        self.assertTrue(king.can_reach(self.board, (3, 3)))

    def test_can_reach_pawn(self):
        king = King(self.white, (4, 0))
        pawn = Pawn(self.white, (4, 1))
        self.board.add_piece(king)
        self.board.add_piece(pawn)
        self.assertTrue(pawn.can_reach(self.board, (4, 2)))

    def test_can_reach_pawn2(self):
        king = King(self.white, (4, 0))
        pawn = Pawn(self.white, (4, 1))
        self.board.add_piece(king)
        self.board.add_piece(pawn)
        self.assertTrue(pawn.can_reach(self.board, (4, 3)))

    def test_can_reach_castle_king(self):
        rook1 = Rook(self.white, (0, 0))
        king = King(self.white, (4, 0))
        rook2 = Rook(self.white, (7, 0))
        self.board.add_piece(king)
        self.board.add_piece(rook1)
        self.board.add_piece(rook2)
        self.assertTrue(king.can_reach(self.board, (6, 0)))

    def test_can_reach_castle_queen(self):
        rook1 = Rook(self.white, (0, 0))
        king = King(self.white, (4, 0))
        rook2 = Rook(self.white, (7, 0))
        self.board.add_piece(king)
        self.board.add_piece(rook1)
        self.board.add_piece(rook2)
        self.assertTrue(king.can_reach(self.board, (2, 0)))

    def test_cant_reach(self):
        king = King(self.white, (4, 4))
        self.board.add_piece(king)
        self.assertFalse(king.can_reach(self.board, (2, 2)))


class KnightTest(ChessTest):
    def test_moves_center(self):
        knight = Knight(self.white, (4, 4))
        moves = list(knight.moves(self.board))
        self.assertEquals(len(moves), 8)

    def test_moves_corner(self):
        knight = Knight(self.white, (0, 0))
        moves = list(knight.moves(self.board))
        self.assertEquals(len(moves), 2)

    def test_moves_blocked_ally(self):
        knight = Knight(self.white, (0, 0))
        bishop = Bishop(self.white, (1, 2))
        self.board.add_piece(bishop)
        moves = list(knight.moves(self.board))
        self.assertEquals(len(moves), 1)

    def test_moves_blocked_enemy(self):
        knight = Knight(self.white, (0, 0))
        bishop = Bishop(self.black, (1, 2))
        self.board.add_piece(bishop)
        moves = list(knight.moves(self.board))
        self.assertEquals(len(moves), 2)

    def test_can_reach_normal(self):
        knight = Knight(self.white, (0, 0))
        self.assertTrue(knight.can_reach(self.board, (1, 2)))


class RookTest(ChessTest):
    def test_moves_center(self):
        king = King(self.white, (3, 3))
        rook = Rook(self.white, (4, 4))
        self.board.add_piece(king)
        self.board.add_piece(rook)
        moves = list(rook.moves(self.board))
        self.assertEquals(len(moves), 14, moves)

    def test_moves_corner(self):
        king = King(self.white, (3, 3))
        rook = Rook(self.white, (0, 0))
        self.board.add_piece(king)
        self.board.add_piece(rook)
        moves = list(rook.moves(self.board))
        self.assertEquals(len(moves), 14, moves)

    def test_moves_blocked_ally(self):
        rook = Rook(self.white, (0, 0))
        king = King(self.white, (0, 1))
        self.board.add_piece(rook)
        self.board.add_piece(king)
        moves = list(rook.moves(self.board))
        self.assertEquals(len(moves), 7, moves)

    def test_moves_blocked_enemy(self):
        rook = Rook(self.white, (0, 0))
        knight = Knight(self.black, (0, 1))
        self.board.add_piece(rook)
        self.board.add_piece(knight)
        moves = list(rook.moves(self.board))
        self.assertEquals(len(moves), 8, moves)


class BishopTest(ChessTest):
    def test_moves_center(self):
        bishop = Bishop(self.white, (4, 4))
        self.board.add_piece(bishop)
        moves = list(bishop.moves(self.board))
        self.assertEquals(len(moves), 13, moves)

    def test_moves_corner(self):
        bishop = Bishop(self.white, (0, 0))
        self.board.add_piece(bishop)
        moves = list(bishop.moves(self.board))
        self.assertEquals(len(moves), 7, moves)

    def test_moves_blocked_ally(self):
        bishop = Bishop(self.white, (0, 0))
        knight = Knight(self.white, (1, 1))
        self.board.add_piece(bishop)
        self.board.add_piece(knight)
        moves = list(bishop.moves(self.board))
        self.assertEquals(len(moves), 0, moves)

    def test_moves_blocked_enemy(self):
        bishop = Bishop(self.white, (0, 0))
        knight = Knight(self.black, (1, 1))
        self.board.add_piece(bishop)
        self.board.add_piece(knight)
        moves = list(bishop.moves(self.board))
        self.assertEquals(len(moves), 1, moves)


class QueenTest(ChessTest):
    def test_moves_center(self):
        queen = Queen(self.white, (4, 4))
        self.board.add_piece(queen)
        moves = [_ for _ in queen.moves(self.board)]
        self.assertEquals(len(moves), 13 + 14, moves)

    def test_moves_corner(self):
        queen = Queen(self.white, (0, 0))
        self.board.add_piece(queen)
        moves = [_ for _ in queen.moves(self.board)]
        self.assertEquals(len(moves), 21, moves)

    def test_moves_blocked_ally(self):
        queen = Queen(self.white, (0, 0))
        king = King(self.white, (1, 1))
        self.board.add_piece(queen)
        self.board.add_piece(king)
        moves = [_ for _ in queen.moves(self.board)]
        self.assertEquals(len(moves), 14, moves)

    def test_moves_blocked_enemy(self):
        queen = Queen(self.white, (0, 0))
        king = King(self.black, (1, 1))
        self.board.add_piece(queen)
        self.board.add_piece(king)
        moves = [_ for _ in queen.moves(self.board)]
        self.assertEquals(len(moves), 15, moves)


if __name__ == "__main__":
    unittest.main()
