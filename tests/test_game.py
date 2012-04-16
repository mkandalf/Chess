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


class GameTest(unittest.TestCase):
    def setUp(self):
        self.game = Game(Board())
        self.game.from_fen(\
                "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def test_ply(self):
        expected = 0
        got = self.game.ply
        self.assertEquals(got, expected)

    def test_pieces(self):
        expected = "Knight"
        got = str(self.game.board.piece_at((1, 0)))
        self.assertEquals(got, expected)


class PerftTest(ChessTest):
    def setUp(self):
        super(PerftTest, self).setUp()
        self.game.from_fen(\
                "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1")
        self.game.ply = 0

    def test_perft1(self):
        self.assertEquals(2039, self.game.perft(2))

    def test_divide(self):
        self.game.divide(2)
        self.assertTrue(True)


class MakeMoveTest(ChessTest):
    def test_en_passant(self):
        pawn1 = Pawn(self.white, (4, 4))
        pawn2 = Pawn(self.black, (3, 6))
        self.board.add_piece(pawn1)
        self.board.add_piece(pawn2)
        move = Move(pawn2, pawn2.location, (3, 4))
        self.game._make_move(move)
        self.assertTrue(pawn2.just_moved)

    def test__make_move(self):
        king = King(self.white, (1, 1))
        self.board.add_piece(king)
        self.game._make_move(Move(king, (1, 1), (2, 2)))
        self.assertEquals(king.location, (2, 2))

    def test__make_move_capture(self):
        king = King(self.white, (1, 1))
        knight = Knight(self.black, (2, 2))
        self.board.add_piece(king)
        self.board.add_piece(knight)
        self.game._make_move(Move(king, (1, 1), (2, 2), knight))
        self.assertTrue(knight not in self.board.pieces)

    def test__make_move_promotion_pawn_removed(self):
        pawn = Pawn(self.white, (0, 6))
        self.board.add_piece(pawn)
        self.game._make_move(Move(pawn, (0, 6), (0, 7), None, Queen))
        self.assertTrue(pawn not in self.board.pieces,
                (pawn, self.board.pieces, pawn in self.board.pieces))

    def test__make_move_promotion_piece_added(self):
        pawn = Pawn(self.white, (0, 6))
        self.board.add_piece(pawn)
        self.game._make_move(Move(pawn, (0, 6), (0, 7), None, Queen))
        for piece in self.board.pieces:
            queen = piece
            break
        self.assertTrue(queen in self.board.pieces)

    def test__make_move_promotion_queen_added(self):
        pawn = Pawn(self.white, (0, 6))
        self.board.add_piece(pawn)
        self.game._make_move(Move(pawn, (0, 6), (0, 7), None, Queen))
        queen = self.board.pieces.pop()
        self.assertEquals(queen, Queen(self.white, (0, 7)))

    def test_promotion_by_capture_pawn_is_removed(self):
        pawn = Pawn(self.white, (0, 6))
        queen = Queen(self.black, (1, 7))
        self.board.add_piece(pawn)
        self.board.add_piece(queen)
        move = Move(pawn, (0, 6), (1, 7), queen, Queen)
        self.game._make_move(move)
        self.assertFalse(pawn in self.board.pieces)

    def test_promotion_by_capture_captured_is_removed(self):
        pawn = Pawn(self.white, (0, 6))
        queen = Queen(self.black, (1, 7))
        self.board.add_piece(pawn)
        self.board.add_piece(queen)
        move = Move(pawn, (0, 6), (1, 7), queen, Queen)
        self.game._make_move(move)
        self.assertFalse(queen in self.board.pieces)


class UndoMoveTest(ChessTest):

    def test__make_move(self):
        king = King(self.white, (1, 1))
        self.board.add_piece(king)
        move = Move(king, (1, 1), (2, 2))
        self.game._make_move(move)
        self.game._undo_move()
        self.assertEquals(king.location, (1, 1))

    def test__make_move_capture(self):
        king = King(self.white, (1, 1))
        knight = Knight(self.black, (2, 2))
        self.board.add_piece(king)
        self.board.add_piece(knight)
        move = Move(king, (1, 1), (2, 2), knight)
        self.game._make_move(move)
        self.game._undo_move()
        self.assertTrue(knight in self.board.pieces)

    def test__make_move_promotion_pawn_removed(self):
        pawn = Pawn(self.white, (0, 6))
        self.board.add_piece(pawn)
        move = Move(pawn, (0, 6), (0, 7), None, Queen)
        self.game._make_move(move)
        self.game._undo_move()
        self.assertTrue(pawn in self.board.pieces)

    def test__make_move_promotion_piece_added(self):
        pawn = Pawn(self.white, (0, 6))
        self.board.add_piece(pawn)
        move = Move(pawn, (0, 6), (0, 7), None, Queen)
        self.game._make_move(move)
        self.game._undo_move()
        self.assertTrue(all(type(piece) != Queen for piece \
                in self.board.pieces))

    def test_promotion_by_capture_pawn_is_restored(self):
        pawn = Pawn(self.white, (0, 6))
        queen = Queen(self.black, (1, 7))
        self.board.add_piece(pawn)
        self.board.add_piece(queen)
        move = Move(pawn, (0, 6), (1, 7), queen, Queen)
        self.game._make_move(move)
        self.game._undo_move()
        self.assertTrue(move.piece in self.board.pieces)

    def test_promotion_by_capture_captured_is_restored(self):
        pawn = Pawn(self.white, (0, 6))
        queen = Queen(self.black, (1, 7))
        self.board.add_piece(pawn)
        self.board.add_piece(queen)
        move = Move(pawn, (0, 6), (1, 7), queen, Queen)
        self.game._make_move(move)
        self.game._undo_move()
        self.assertTrue(move.captured in self.board.pieces)

    def test_en_passant(self):
        pawn1 = Pawn(self.white, (4, 4))
        pawn2 = Pawn(self.black, (3, 6))
        self.board.add_piece(pawn1)
        self.board.add_piece(pawn2)
        move = Move(pawn2, pawn2.location, (3, 4))
        pieces = list(self.board.pieces)
        self.game._make_move(move)
        self.game._undo_move()
        self.assertEquals(pieces, self.board.pieces)


class IsLegalTest(ChessTest):
    def test_moves_not_check(self):
        king = King(self.white, (1, 1))
        self.board.add_piece(king)
        move = Move(king, (1, 1), (2, 2))
        self.assertTrue(self.game.is_legal(move))

    def test_moves_is_check(self):
        king = King(self.white, (1, 1))
        knight = Knight(self.black, (0, 0))
        self.board.add_piece(king)
        self.board.add_piece(knight)
        move = Move(king, (1, 1), (1, 2))
        self.assertFalse(self.game.is_legal(move))


class IsOverTest(ChessTest):
    def test_over(self):
        self.white.castling.append((False, False))
        king = King(self.white, (0, 0))
        rook1 = Rook(self.black, (8, 0))
        rook2 = Rook(self.black, (8, 1))
        self.board.add_piece(king)
        self.board.add_piece(rook1)
        self.board.add_piece(rook2)
        self.assertTrue(self.game.is_over)

    def test_not_over(self):
        self.white.castling.append((False, False))
        king = King(self.white, (0, 0))
        rook1 = Rook(self.black, (8, 0))
        king2 = King(self.black, (7, 0))
        self.board.add_piece(king)
        self.board.add_piece(rook1)
        self.board.add_piece(king2)
        self.assertFalse(self.game.is_over)


class StalemateTest(ChessTest):
    def test_not_stalemate(self):
        self.white.castling.append((False, False))
        king = King(self.white, (0, 0))
        rook1 = Rook(self.black, (8, 0))
        rook2 = Rook(self.black, (8, 1))
        self.board.add_piece(king)
        self.board.add_piece(rook1)
        self.board.add_piece(rook2)
        self.assertFalse(self.game.is_stalemate(self.white))

    def test_stalemate(self):
        self.white.castling.append((False, False))
        king = King(self.white, (0, 0))
        rook1 = Rook(self.black, (8, 1))
        rook2 = Rook(self.black, (1, 8))
        self.board.add_piece(king)
        self.board.add_piece(rook1)
        self.board.add_piece(rook2)
        self.assertTrue(self.game.is_stalemate(self.white))


class CheckmateTest(ChessTest):
    def test_not_checkmate(self):
        self.white.castling.append((False, False))
        king = King(self.white, (0, 0))
        rook1 = Rook(self.black, (8, 1))
        rook2 = Rook(self.black, (1, 8))
        self.board.add_piece(king)
        self.board.add_piece(rook1)
        self.board.add_piece(rook2)
        self.assertFalse(self.game.is_checkmate(self.white))

    def test_not_over(self):
        self.white.castling.append((False, False))
        king = King(self.white, (0, 0))
        rook1 = Rook(self.black, (8, 0))
        rook2 = Rook(self.black, (8, 1))
        self.board.add_piece(king)
        self.board.add_piece(rook1)
        self.board.add_piece(rook2)
        self.assertTrue(self.game.is_checkmate(self.white))


if __name__ == "__main__":
    unittest.main()
