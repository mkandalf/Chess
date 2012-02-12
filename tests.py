import unittest

from board import Board
from move import Move
from piece import King, Knight, Rook, Bishop, Queen, Pawn
from player import Player, Color


class ChessTest(unittest.TestCase):
    def setUp(self):
        self.board = Board(set())
        self.white = Player(Color.WHITE)
        self.black = Player(Color.BLACK)


class PlayerTest(ChessTest):
    def test_parse_square_a1(self):
        self.assertEquals((0, 0), self.white._parse_square('a1'))

    def test_parse_square_h8(self):
        self.assertEquals((7, 7), self.white._parse_square('h8'))

    def test_parse_move_no_piece(self):
        expected = Move(None, None, (7, 6), (7, 7))
        got = self.white._parse_move('h7 h8', self.board)
        self.assertEquals(got, expected)

    def test_parse_move_piece(self):
        king = King(self.white, (4, 4))
        self.board.pieces.add(king)
        expected = Move(king, None, (4, 4), (5, 5))
        got = self.white._parse_move('e5 f6', self.board)
        self.assertEquals(got, expected)


class OnBoardTest(ChessTest):
    def test_on_board_center(self):
        self.assertTrue(self.board.on_board((4, 4)))

    def test_on_board_corner1(self):
        self.assertTrue(self.board.on_board((0, 0)))

    def test_on_board_corner2(self):
        self.assertTrue(self.board.on_board((7, 7)))

    def test_off_board(self):
        self.assertFalse(self.board.on_board((8, 8)))


class InCheckTest(ChessTest):
    def test_not_check(self):
        self.board.pieces.add(King(self.white, (4, 4)))
        self.assertFalse(self.board.in_check(self.white))

    def test_in_check(self):
        self.board.pieces.add(King(self.white, (1, 2)))
        self.board.pieces.add(Knight(self.black, (0, 0)))
        self.assertTrue(self.board.in_check(self.white))


class MakeMoveTest(ChessTest):
    def test_make_move(self):
        king = King(self.white, (1, 1))
        self.board.pieces.add(king)
        self.board.make_move(Move(king, None, (1, 1), (2, 2)))
        self.assertEquals(king.location, (2, 2))

    def test_make_move_capture(self):
        king = King(self.white, (1, 1))
        knight = Knight(self.black, (2, 2))
        self.board.pieces.add(king)
        self.board.pieces.add(knight)
        self.board.make_move(Move(king, knight, (1, 1), (2, 2)))
        self.assertTrue(knight not in self.board.pieces)

    def test_make_move_promotion_pawn_removed(self):
        pawn = Pawn(self.white, (0, 6))
        self.board.pieces.add(pawn)
        self.board.make_move(Move(pawn, None, (0, 6), (0, 7), Queen))
        self.assertTrue(pawn not in self.board.pieces)

    def test_make_move_promotion_piece_added(self):
        pawn = Pawn(self.white, (0, 6))
        self.board.pieces.add(pawn)
        self.board.make_move(Move(pawn, None, (0, 6), (0, 7), Queen))
        for piece in self.board.pieces:
            queen = piece
            break
        self.assertTrue(queen in self.board.pieces)

    def test_make_move_promotion_queen_added(self):
        pawn = Pawn(self.white, (0, 6))
        self.board.pieces.add(pawn)
        self.board.make_move(Move(pawn, None, (0, 6), (0, 7), Queen))
        queen = self.board.pieces.pop()
        self.assertEquals(queen, Queen(self.white, (0, 7)))


class UndoMoveTest(ChessTest):
    def test_make_move(self):
        king = King(self.white, (1, 1))
        self.board.pieces.add(king)
        move = Move(king, None, (1, 1), (2, 2))
        self.board.make_move(move)
        self.board.undo_move(move)
        self.assertEquals(king.location, (1, 1))

    def test_make_move_capture(self):
        king = King(self.white, (1, 1))
        knight = Knight(self.black, (2, 2))
        self.board.pieces.add(king)
        self.board.pieces.add(knight)
        move = Move(king, knight, (1, 1), (2, 2))
        self.board.make_move(move)
        self.board.undo_move(move)
        self.assertTrue(knight in self.board.pieces)

    def test_make_move_promotion_pawn_removed(self):
        pawn = Pawn(self.white, (0, 6))
        self.board.pieces.add(pawn)
        move = Move(pawn, None, (0, 6), (0, 7), Queen)
        self.board.make_move(move)
        self.board.undo_move(move)
        self.assertTrue(any(piece == pawn for piece in self.board.pieces))

    def test_make_move_promotion_piece_added(self):
        pawn = Pawn(self.white, (0, 6))
        self.board.pieces.add(pawn)
        move = Move(pawn, None, (0, 6), (0, 7), Queen)
        self.board.make_move(move)
        self.board.undo_move(move)
        self.assertTrue(all(type(piece) != Queen for piece \
                in self.board.pieces))


class IsLegalTest(ChessTest):
    def test_reachable_not_check(self):
        king = King(self.white, (1, 1))
        self.board.pieces.add(king)
        move = Move(king, None, (1, 1), (2, 2))
        self.assertTrue(self.board.is_legal(move))

    def test_not_reachable_not_check(self):
        king = King(self.white, (1, 1))
        self.board.pieces.add(king)
        move = Move(king, None, (1, 1), (3, 3))
        self.assertFalse(self.board.is_legal(move))

    def test_reachable_is_check(self):
        king = King(self.white, (1, 1))
        knight = Knight(self.black, (0, 0))
        self.board.pieces.add(king)
        self.board.pieces.add(knight)
        move = Move(king, None, (1, 1), (1, 2))
        self.assertFalse(self.board.is_legal(move))


class MovesTest(ChessTest):
    def test_simple(self):
        king = King(self.white, (1, 1))
        self.board.pieces.add(king)
        piece_moves = set([m for m in king.moves(self.board)])
        assert king.location == (1, 1), king.location
        board_moves = set([m for m in self.board.moves(self.white)])
        self.assertEquals(len(piece_moves), len(board_moves),
                (piece_moves, board_moves))


class IsOverTest(ChessTest):
    def test_over(self):
        king = King(self.white, (0, 0))
        rook1 = Rook(self.black, (8, 0))
        rook2 = Rook(self.black, (8, 1))
        self.board.pieces.add(king)
        self.board.pieces.add(rook1)
        self.board.pieces.add(rook2)
        self.assertTrue(self.board.is_over(self.white))

    def test_not_over(self):
        king = King(self.white, (0, 0))
        rook1 = Rook(self.black, (8, 0))
        self.board.pieces.add(king)
        self.board.pieces.add(rook1)
        self.assertFalse(self.board.is_over(self.white))


class StalemateTest(ChessTest):
    def test_not_stalemate(self):
        king = King(self.white, (0, 0))
        rook1 = Rook(self.black, (8, 0))
        rook2 = Rook(self.black, (8, 1))
        self.board.pieces.add(king)
        self.board.pieces.add(rook1)
        self.board.pieces.add(rook2)
        self.assertFalse(self.board.is_stalemate(self.white))

    def test_stalemate(self):
        king = King(self.white, (0, 0))
        rook1 = Rook(self.black, (8, 1))
        rook2 = Rook(self.black, (1, 8))
        self.board.pieces.add(king)
        self.board.pieces.add(rook1)
        self.board.pieces.add(rook2)
        self.assertTrue(self.board.is_stalemate(self.white))


class CheckmateTest(ChessTest):
    def test_not_checkmate(self):
        king = King(self.white, (0, 0))
        rook1 = Rook(self.black, (8, 1))
        rook2 = Rook(self.black, (1, 8))
        self.board.pieces.add(king)
        self.board.pieces.add(rook1)
        self.board.pieces.add(rook2)
        self.assertFalse(self.board.is_checkmate(self.white))

    def test_not_over(self):
        king = King(self.white, (0, 0))
        rook1 = Rook(self.black, (8, 0))
        rook2 = Rook(self.black, (8, 1))
        self.board.pieces.add(king)
        self.board.pieces.add(rook1)
        self.board.pieces.add(rook2)
        self.assertTrue(self.board.is_checkmate(self.white))


class PieceAtTest(ChessTest):
    def test_no_piece(self):
        self.assertEquals(self.board.piece_at((0, 0)), None)

    def test_piece(self):
        king = King(self.white, (0, 0))
        self.board.pieces.add(king)
        self.assertEquals(self.board.piece_at((0, 0)), king)


class PawnTest(ChessTest):
    def test_reachable_center(self):
        pawn = Pawn(self.white, (4, 4))
        reachable = list(pawn.reachable(self.board))
        self.assertEquals(len(reachable), 1, reachable)

    def test_reachable_start(self):
        pawn = Pawn(self.white, (4, 1))
        reachable = list(pawn.reachable(self.board))
        self.assertEquals(len(reachable), 2, reachable)

    def test_reachable_start_blocked(self):
        pawn = Pawn(self.white, (4, 1))
        bishop = Bishop(self.white, (4, 3))
        self.board.pieces.add(bishop)
        reachable = list(pawn.reachable(self.board))
        self.assertEquals(len(reachable), 1, reachable)

    def test_reachable_blocked_ally(self):
        pawn = Pawn(self.white, (4, 4))
        bishop = Bishop(self.white, (4, 5))
        self.board.pieces.add(bishop)
        reachable = list(pawn.reachable(self.board))
        self.assertEquals(len(reachable), 0, reachable)

    def test_reachable_blocked_enemy(self):
        pawn = Pawn(self.white, (4, 4))
        bishop = Bishop(self.black, (4, 5))
        self.board.pieces.add(bishop)
        reachable = list(pawn.reachable(self.board))
        self.assertEquals(len(reachable), 0, reachable)

    def test_reachable_captureable_enemy(self):
        pawn = Pawn(self.white, (4, 4))
        bishop = Bishop(self.black, (5, 5))
        self.board.pieces.add(bishop)
        reachable = list(pawn.reachable(self.board))
        self.assertEquals(len(reachable), 2, reachable)

    def test_promotions(self):
        pawn = Pawn(self.white, (4, 6))
        moves = list(pawn.moves(self.board))
        self.assertEquals(len(moves), 4, moves)


class KingTest(ChessTest):
    def test_reachable_center(self):
        king = King(self.white, (4, 4))
        reachable = list(king.reachable(self.board))
        self.assertEquals(len(reachable), 8, reachable)

    def test_reachable_blocked_ally(self):
        king = King(self.white, (4, 4))
        knight = Knight(self.white, (3, 3))
        self.board.pieces.add(knight)
        reachable = list(king.reachable(self.board))
        self.assertEquals(len(reachable), 7, reachable)

    def test_reachable_blocked_enemy(self):
        king = King(self.white, (4, 4))
        knight = Knight(self.black, (3, 3))
        self.board.pieces.add(knight)
        reachable = list(king.reachable(self.board))
        self.assertEquals(len(reachable), 8, reachable)

    def test_reachable_corner(self):
        king = King(self.white, (0, 0))
        reachable = list(king.reachable(self.board))
        self.assertEquals(len(reachable), 3, reachable)

    def test_can_reach_normal(self):
        king = King(self.white, (4, 4))
        self.assertTrue(king.can_reach(self.board, (3, 3)))

    def test_cant_reach(self):
        king = King(self.white, (4, 4))
        self.assertFalse(king.can_reach(self.board, (2, 2)))


class KnightTest(ChessTest):
    def test_reachable_center(self):
        knight = Knight(self.white, (4, 4))
        reachable = list(knight.reachable(self.board))
        self.assertEquals(len(reachable), 8)

    def test_reachable_corner(self):
        knight = Knight(self.white, (0, 0))
        reachable = list(knight.reachable(self.board))
        self.assertEquals(len(reachable), 2)

    def test_reachable_blocked_ally(self):
        knight = Knight(self.white, (0, 0))
        bishop = Bishop(self.white, (1, 2))
        self.board.pieces.add(bishop)
        reachable = list(knight.reachable(self.board))
        self.assertEquals(len(reachable), 1)

    def test_reachable_blocked_enemy(self):
        knight = Knight(self.white, (0, 0))
        bishop = Bishop(self.black, (1, 2))
        self.board.pieces.add(bishop)
        reachable = list(knight.reachable(self.board))
        self.assertEquals(len(reachable), 2)

    def test_can_reach_normal(self):
        knight = Knight(self.white, (0, 0))
        self.assertTrue(knight.can_reach(self.board, (1, 2)))


class RookTest(ChessTest):
    def test_reachable_center(self):
        rook = Rook(self.white, (4, 4))
        self.board.pieces.add(rook)
        reachable = list(rook.reachable(self.board))
        self.assertEquals(len(reachable), 14, reachable)

    def test_reachable_corner(self):
        rook = Rook(self.white, (0, 0))
        self.board.pieces.add(rook)
        reachable = list(rook.reachable(self.board))
        self.assertEquals(len(reachable), 14, reachable)

    def test_reachable_blocked_ally(self):
        rook = Rook(self.white, (0, 0))
        knight = Knight(self.white, (0, 1))
        self.board.pieces.add(rook)
        self.board.pieces.add(knight)
        reachable = list(rook.reachable(self.board))
        self.assertEquals(len(reachable), 7, reachable)

    def test_reachable_blocked_enemy(self):
        rook = Rook(self.white, (0, 0))
        knight = Knight(self.black, (0, 1))
        self.board.pieces.add(rook)
        self.board.pieces.add(knight)
        reachable = list(rook.reachable(self.board))
        self.assertEquals(len(reachable), 8, reachable)


class BishopTest(ChessTest):
    def test_reachable_center(self):
        bishop = Bishop(self.white, (4, 4))
        self.board.pieces.add(bishop)
        reachable = list(bishop.reachable(self.board))
        self.assertEquals(len(reachable), 13, reachable)

    def test_reachable_corner(self):
        bishop = Bishop(self.white, (0, 0))
        self.board.pieces.add(bishop)
        reachable = list(bishop.reachable(self.board))
        self.assertEquals(len(reachable), 7, reachable)

    def test_reachable_blocked_ally(self):
        bishop = Bishop(self.white, (0, 0))
        knight = Knight(self.white, (1, 1))
        self.board.pieces.add(bishop)
        self.board.pieces.add(knight)
        reachable = list(bishop.reachable(self.board))
        self.assertEquals(len(reachable), 0, reachable)

    def test_reachable_blocked_enemy(self):
        bishop = Bishop(self.white, (0, 0))
        knight = Knight(self.black, (1, 1))
        self.board.pieces.add(bishop)
        self.board.pieces.add(knight)
        reachable = list(bishop.reachable(self.board))
        self.assertEquals(len(reachable), 1, reachable)


class QueenTest(ChessTest):
    def test_reachable_center(self):
        queen = Queen(self.white, (4, 4))
        self.board.pieces.add(queen)
        reachable = [_ for _ in queen.reachable(self.board)]
        self.assertEquals(len(reachable), 13 + 14, reachable)

    def test_reachable_corner(self):
        queen = Queen(self.white, (0, 0))
        self.board.pieces.add(queen)
        reachable = [_ for _ in queen.reachable(self.board)]
        self.assertEquals(len(reachable), 21, reachable)

    def test_reachable_blocked_ally(self):
        queen = Queen(self.white, (0, 0))
        king = King(self.white, (1, 1))
        self.board.pieces.add(queen)
        self.board.pieces.add(king)
        reachable = [_ for _ in queen.reachable(self.board)]
        self.assertEquals(len(reachable), 14, reachable)

    def test_reachable_blocked_enemy(self):
        queen = Queen(self.white, (0, 0))
        king = King(self.black, (1, 1))
        self.board.pieces.add(queen)
        self.board.pieces.add(king)
        reachable = [_ for _ in queen.reachable(self.board)]
        self.assertEquals(len(reachable), 15, reachable)


if __name__ == "__main__":
    unittest.main()
