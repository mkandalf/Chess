import unittest

from board import Board
from color import Color
from move import Move
from player import Player
from game import Game
from piece import King, Knight, Rook, Bishop, Queen, Pawn


class ChessTest(unittest.TestCase):
    def setUp(self):
        self.board = Board(set())
        self.white = Player(Color.WHITE)
        self.black = Player(Color.BLACK)
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


class PlayerTest(ChessTest):
    def test_parse_square_a1(self):
        self.assertEquals((0, 0), self.white._parse_square('a1'))

    def test_parse_square_h8(self):
        self.assertEquals((7, 7), self.white._parse_square('h8'))

    def test_parse_move_no_piece(self):
        expected = Move(None, (7, 6), (7, 7))
        got = self.white._parse_move('h7 h8', self.board)
        self.assertEquals(got, expected)

    def test_parse_move_piece(self):
        king = King(self.white, (4, 4))
        self.board.pieces.add(king)
        expected = Move(king, (4, 4), (5, 5))
        got = self.white._parse_move('e5 f6', self.board)
        self.assertEquals(got, expected)

    def test_parse_move_promotion(self):
        pawn = Pawn(self.white, (0, 6))
        self.board.pieces.add(pawn)
        expected = Move(pawn, (0, 6), (0, 7), None, Queen)
        got = self.white._parse_move('a7 a8 Q', self.board)
        self.assertEquals(got, expected)


class OnBoardTest(ChessTest):
    def test_is_on_board_center(self):
        self.assertTrue(self.board.is_on_board((4, 4)))

    def test_is_on_board_corner1(self):
        self.assertTrue(self.board.is_on_board((0, 0)))

    def test_is_on_board_corner2(self):
        self.assertTrue(self.board.is_on_board((7, 7)))

    def test_off_board(self):
        self.assertFalse(self.board.is_on_board((8, 8)))


class InCheckTest(ChessTest):
    def test_not_check(self):
        self.board.pieces.add(King(self.white, (4, 4)))
        self.assertFalse(self.white.is_in_check(self.board))

    def test_not_check_pawn(self):
        self.board.pieces.add(King(self.white, (4, 4)))
        self.board.pieces.add(Pawn(self.black, (4, 5)))
        self.assertFalse(self.white.is_in_check(self.board))

    def test_not_check_pawn_unmoved(self):
        self.board.pieces.add(King(self.white, (4, 5)))
        self.board.pieces.add(Pawn(self.black, (4, 7)))
        self.assertFalse(self.white.is_in_check(self.board))

    def test_is_in_check(self):
        self.board.pieces.add(King(self.white, (1, 2)))
        self.board.pieces.add(Knight(self.black, (0, 0)))
        self.assertTrue(self.white.is_in_check(self.board))


class MakeMoveTest(ChessTest):
    def test_en_passant(self):
        pawn1 = Pawn(self.white, (4, 4))
        pawn2 = Pawn(self.black, (3, 6))
        self.board.pieces.add(pawn1)
        self.board.pieces.add(pawn2)
        move = Move(pawn2, pawn2.location, (3, 4))
        self.game.make_move(move)
        self.assertTrue(pawn2.just_moved)

    def test_make_move(self):
        king = King(self.white, (1, 1))
        self.board.pieces.add(king)
        self.game.make_move(Move(king, (1, 1), (2, 2)))
        self.assertEquals(king.location, (2, 2))

    def test_make_move_capture(self):
        king = King(self.white, (1, 1))
        knight = Knight(self.black, (2, 2))
        self.board.pieces.add(king)
        self.board.pieces.add(knight)
        self.game.make_move(Move(king, (1, 1), (2, 2), knight))
        self.assertTrue(knight not in self.board.pieces)

    def test_make_move_promotion_pawn_removed(self):
        pawn = Pawn(self.white, (0, 6))
        self.board.pieces.add(pawn)
        self.game.make_move(Move(pawn, (0, 6), (0, 7), None, Queen))
        self.assertTrue(pawn not in self.board.pieces)

    def test_make_move_promotion_piece_added(self):
        pawn = Pawn(self.white, (0, 6))
        self.board.pieces.add(pawn)
        self.game.make_move(Move(pawn, (0, 6), (0, 7), None, Queen))
        for piece in self.board.pieces:
            queen = piece
            break
        self.assertTrue(queen in self.board.pieces)

    def test_make_move_promotion_queen_added(self):
        pawn = Pawn(self.white, (0, 6))
        self.board.pieces.add(pawn)
        self.game.make_move(Move(pawn, (0, 6), (0, 7), None, Queen))
        queen = self.board.pieces.pop()
        self.assertEquals(queen, Queen(self.white, (0, 7)))

    def test_promotion_by_capture_pawn_is_removed(self):
        pawn = Pawn(self.white, (0, 6))
        queen = Queen(self.black, (1, 7))
        self.board.pieces.add(pawn)
        self.board.pieces.add(queen)
        move = Move(pawn, (0, 6), (1, 7), queen, Queen)
        self.game.make_move(move)
        self.assertFalse(pawn in self.board.pieces)

    def test_promotion_by_capture_captured_is_removed(self):
        pawn = Pawn(self.white, (0, 6))
        queen = Queen(self.black, (1, 7))
        self.board.pieces.add(pawn)
        self.board.pieces.add(queen)
        move = Move(pawn, (0, 6), (1, 7), queen, Queen)
        self.game.make_move(move)
        self.assertFalse(queen in self.board.pieces)


class UndoMoveTest(ChessTest):

    def test_make_move(self):
        king = King(self.white, (1, 1))
        self.board.pieces.add(king)
        move = Move(king, (1, 1), (2, 2))
        self.game.make_move(move)
        self.game.undo_move()
        self.assertEquals(king.location, (1, 1))

    def test_make_move_capture(self):
        king = King(self.white, (1, 1))
        knight = Knight(self.black, (2, 2))
        self.board.pieces.add(king)
        self.board.pieces.add(knight)
        move = Move(king, (1, 1), (2, 2), knight)
        self.game.make_move(move)
        self.game.undo_move()
        self.assertTrue(knight in self.board.pieces)

    def test_make_move_promotion_pawn_removed(self):
        pawn = Pawn(self.white, (0, 6))
        self.board.pieces.add(pawn)
        move = Move(pawn, (0, 6), (0, 7), None, Queen)
        self.game.make_move(move)
        self.game.undo_move()
        self.assertTrue(pawn in self.board.pieces)

    def test_make_move_promotion_piece_added(self):
        pawn = Pawn(self.white, (0, 6))
        self.board.pieces.add(pawn)
        move = Move(pawn, (0, 6), (0, 7), None, Queen)
        self.game.make_move(move)
        self.game.undo_move()
        self.assertTrue(all(type(piece) != Queen for piece \
                in self.board.pieces))

    def test_promotion_by_capture_pawn_is_restored(self):
        pawn = Pawn(self.white, (0, 6))
        queen = Queen(self.black, (1, 7))
        self.board.pieces.add(pawn)
        self.board.pieces.add(queen)
        move = Move(pawn, (0, 6), (1, 7), queen, Queen)
        self.game.make_move(move)
        self.game.undo_move()
        self.assertTrue(move.piece in self.board.pieces)

    def test_promotion_by_capture_captured_is_restored(self):
        pawn = Pawn(self.white, (0, 6))
        queen = Queen(self.black, (1, 7))
        self.board.pieces.add(pawn)
        self.board.pieces.add(queen)
        move = Move(pawn, (0, 6), (1, 7), queen, Queen)
        self.game.make_move(move)
        self.game.undo_move()
        self.assertTrue(move.captured in self.board.pieces)

    def test_en_passant(self):
        pawn1 = Pawn(self.white, (4, 4))
        pawn2 = Pawn(self.black, (3, 6))
        self.board.pieces.add(pawn1)
        self.board.pieces.add(pawn2)
        move = Move(pawn2, pawn2.location, (3, 4))
        pieces = set(self.board.pieces)
        self.game.make_move(move)
        self.game.undo_move()
        self.assertEquals(pieces, self.board.pieces)


class IsLegalTest(ChessTest):
    def test_moves_not_check(self):
        king = King(self.white, (1, 1))
        self.board.pieces.add(king)
        move = Move(king, (1, 1), (2, 2))
        self.assertTrue(self.game.is_legal(move))

    def test_not_moves_not_check(self):
        king = King(self.white, (1, 1))
        self.board.pieces.add(king)
        move = Move(king, (1, 1), (3, 3))
        self.assertFalse(self.game.is_legal(move))

    def test_moves_is_check(self):
        king = King(self.white, (1, 1))
        knight = Knight(self.black, (0, 0))
        self.board.pieces.add(king)
        self.board.pieces.add(knight)
        move = Move(king, (1, 1), (1, 2))
        self.assertFalse(self.game.is_legal(move))


class MovesTest(ChessTest):
    def test_simple(self):
        self.white.castling.append((False, False))
        king = King(self.white, (1, 1))
        self.board.pieces.add(king)
        piece_moves = set([m for m in king.moves(self.board)])
        assert king.location == (1, 1), king.location
        board_moves = set([m for m in self.white.moves(self.board)])
        self.assertEquals(len(piece_moves), len(board_moves),
                (piece_moves, board_moves))


class IsOverTest(ChessTest):
    def test_over(self):
        self.white.castling.append((False, False))
        king = King(self.white, (0, 0))
        rook1 = Rook(self.black, (8, 0))
        rook2 = Rook(self.black, (8, 1))
        self.board.pieces.add(king)
        self.board.pieces.add(rook1)
        self.board.pieces.add(rook2)
        self.assertTrue(self.game.is_over)

    def test_not_over(self):
        self.white.castling.append((False, False))
        king = King(self.white, (0, 0))
        rook1 = Rook(self.black, (8, 0))
        self.board.pieces.add(king)
        self.board.pieces.add(rook1)
        self.assertFalse(self.game.is_over)


class StalemateTest(ChessTest):
    def test_not_stalemate(self):
        self.white.castling.append((False, False))
        king = King(self.white, (0, 0))
        rook1 = Rook(self.black, (8, 0))
        rook2 = Rook(self.black, (8, 1))
        self.board.pieces.add(king)
        self.board.pieces.add(rook1)
        self.board.pieces.add(rook2)
        self.assertFalse(self.game.is_stalemate(self.white))

    def test_stalemate(self):
        self.white.castling.append((False, False))
        king = King(self.white, (0, 0))
        rook1 = Rook(self.black, (8, 1))
        rook2 = Rook(self.black, (1, 8))
        self.board.pieces.add(king)
        self.board.pieces.add(rook1)
        self.board.pieces.add(rook2)
        self.assertTrue(self.game.is_stalemate(self.white))


class CheckmateTest(ChessTest):
    def test_not_checkmate(self):
        self.white.castling.append((False, False))
        king = King(self.white, (0, 0))
        rook1 = Rook(self.black, (8, 1))
        rook2 = Rook(self.black, (1, 8))
        self.board.pieces.add(king)
        self.board.pieces.add(rook1)
        self.board.pieces.add(rook2)
        self.assertFalse(self.game.is_checkmate(self.white))

    def test_not_over(self):
        self.white.castling.append((False, False))
        king = King(self.white, (0, 0))
        rook1 = Rook(self.black, (8, 0))
        rook2 = Rook(self.black, (8, 1))
        self.board.pieces.add(king)
        self.board.pieces.add(rook1)
        self.board.pieces.add(rook2)
        self.assertTrue(self.game.is_checkmate(self.white))


class PieceAtTest(ChessTest):
    def test_no_piece(self):
        self.assertEquals(self.board.piece_at((0, 0)), None)

    def test_piece(self):
        king = King(self.white, (0, 0))
        self.board.pieces.add(king)
        self.assertEquals(self.board.piece_at((0, 0)), king)


class PawnTest(ChessTest):
    def test_en_passant(self):
        pawn1 = Pawn(self.white, (4, 4))
        pawn2 = Pawn(self.black, (3, 6))
        self.board.pieces.add(pawn1)
        self.board.pieces.add(pawn2)
        move = Move(pawn2, pawn2.location, (3, 4))
        self.game.make_move(move)
        moves = [m for m in pawn1.moves(self.board)]
        self.assertEqual(len(moves), 2)

    def test_cant_en_passant(self):
        pawn1 = Pawn(self.white, (4, 4))
        pawn2 = Pawn(self.black, (3, 5))
        self.board.pieces.add(pawn1)
        self.board.pieces.add(pawn2)
        move = Move(pawn2, pawn2.location, (3, 4))
        self.game.make_move(move)
        moves = [m for m in pawn1.moves(self.board)]
        self.assertEqual(len(moves), 1)

    def test_bad_capture(self):
        self.white.castling.append((False, False))
        pawn1 = Pawn(self.white, (4, 1))
        pawn2 = Pawn(self.white, (5, 1))
        king1 = King(self.white, (4, 0))
        king2 = King(self.black, (4, 7))
        self.board.pieces.add(pawn1)
        self.board.pieces.add(pawn2)
        self.board.pieces.add(king1)
        self.board.pieces.add(king2)
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
        self.board.pieces.add(bishop)
        moves = list(pawn.moves(self.board))
        self.assertEquals(len(moves), 1, moves)

    def test_moves_blocked_ally(self):
        pawn = Pawn(self.white, (4, 4))
        bishop = Bishop(self.white, (4, 5))
        self.board.pieces.add(bishop)
        moves = list(pawn.moves(self.board))
        self.assertEquals(len(moves), 0, moves)

    def test_moves_blocked_enemy(self):
        pawn = Pawn(self.white, (4, 4))
        bishop = Bishop(self.black, (4, 5))
        self.board.pieces.add(bishop)
        moves = list(pawn.moves(self.board))
        self.assertEquals(len(moves), 0, moves)

    def test_moves_captureable_enemy(self):
        king = King(self.white, (0, 4))
        pawn = Pawn(self.white, (4, 4))
        bishop = Bishop(self.black, (5, 5))
        self.board.pieces.add(king)
        self.board.pieces.add(pawn)
        self.board.pieces.add(bishop)
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
        self.board.pieces = set([pawn, rook])
        moves = list(pawn.moves(self.board))
        self.assertTrue(len(moves), 8)

    def test_promotions_are_valid_with_capturable(self):
        pawn = Pawn(self.white, (4, 6))
        rook = Rook(self.black, (3, 7))
        self.board.pieces = set([pawn, rook])
        moves = list(pawn.moves(self.board))
        self.assertTrue(all(move.promotion is not None for move in moves))


class KingTest(ChessTest):
    def test_castle(self):
        rook1 = Rook(self.white, (0, 0))
        king = King(self.white, (4, 0))
        rook2 = Rook(self.white, (7, 0))
        self.board.pieces.add(king)
        self.board.pieces.add(rook1)
        self.board.pieces.add(rook2)
        moves = list(self.white.moves(self.board))
        self.assertEquals(len(moves), 26)

    def test_castle_through_check(self):
        rook1 = Rook(self.white, (0, 0))
        king = King(self.white, (4, 0))
        rook2 = Rook(self.white, (7, 0))
        knight = Knight(self.black, (2, 2))
        self.board.pieces.add(king)
        self.board.pieces.add(rook1)
        self.board.pieces.add(rook2)
        self.board.pieces.add(knight)
        move = Move(king, king.location, (2, 0))
        self.assertFalse(self.game.is_legal(move))

    def test_cant_castle_out_of_check(self):
        king = King(self.white, (4, 0))
        rook1 = Rook(self.white, (0, 0))
        rook2 = Rook(self.black, (4, 7))
        self.board.pieces.add(king)
        self.board.pieces.add(rook1)
        self.board.pieces.add(rook2)
        move = Move(king, king.location, (2, 0))
        self.assertFalse(self.game.is_legal(move))

    def test_moves_center(self):
        self.white.castling.append((False, False))
        king = King(self.white, (4, 4))
        self.board.pieces.add(king)
        moves = list(king.moves(self.board))
        self.assertEquals(len(moves), 8, moves)

    def test_moves_blocked_ally(self):
        self.white.castling.append((False, False))
        king = King(self.white, (4, 4))
        knight = Knight(self.white, (3, 3))
        self.board.pieces.add(king)
        self.board.pieces.add(knight)
        moves = list(king.moves(self.board))
        self.assertEquals(len(moves), 7, moves)

    def test_moves_blocked_enemy(self):
        self.white.castling.append((False, False))
        king = King(self.white, (4, 4))
        knight = Knight(self.black, (3, 3))
        self.board.pieces.add(king)
        self.board.pieces.add(knight)
        moves = list(king.moves(self.board))
        self.assertEquals(len(moves), 8, moves)

    def test_moves_corner(self):
        self.white.castling.append((False, False))
        king = King(self.white, (0, 0))
        self.board.pieces.add(king)
        moves = list(king.moves(self.board))
        self.assertEquals(len(moves), 3, moves)

    def test_can_reach_normal(self):
        king = King(self.white, (4, 4))
        self.board.pieces.add(king)
        self.assertTrue(king.can_reach(self.board, (3, 3)))

    def test_can_reach_pawn(self):
        king = King(self.white, (4, 0))
        pawn = Pawn(self.white, (4, 1))
        self.board.pieces.add(king)
        self.board.pieces.add(pawn)
        self.assertTrue(pawn.can_reach(self.board, (4, 2)))

    def test_can_reach_pawn2(self):
        king = King(self.white, (4, 0))
        pawn = Pawn(self.white, (4, 1))
        self.board.pieces.add(king)
        self.board.pieces.add(pawn)
        self.assertTrue(pawn.can_reach(self.board, (4, 3)))

    def test_can_reach_castle_king(self):
        rook1 = Rook(self.white, (0, 0))
        king = King(self.white, (4, 0))
        rook2 = Rook(self.white, (7, 0))
        self.board.pieces.add(king)
        self.board.pieces.add(rook1)
        self.board.pieces.add(rook2)
        self.assertTrue(king.can_reach(self.board, (6, 0)))

    def test_can_reach_castle_queen(self):
        rook1 = Rook(self.white, (0, 0))
        king = King(self.white, (4, 0))
        rook2 = Rook(self.white, (7, 0))
        self.board.pieces.add(king)
        self.board.pieces.add(rook1)
        self.board.pieces.add(rook2)
        self.assertTrue(king.can_reach(self.board, (2, 0)))

    def test_cant_reach(self):
        king = King(self.white, (4, 4))
        self.board.pieces.add(king)
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
        self.board.pieces.add(bishop)
        moves = list(knight.moves(self.board))
        self.assertEquals(len(moves), 1)

    def test_moves_blocked_enemy(self):
        knight = Knight(self.white, (0, 0))
        bishop = Bishop(self.black, (1, 2))
        self.board.pieces.add(bishop)
        moves = list(knight.moves(self.board))
        self.assertEquals(len(moves), 2)

    def test_can_reach_normal(self):
        knight = Knight(self.white, (0, 0))
        self.assertTrue(knight.can_reach(self.board, (1, 2)))


class RookTest(ChessTest):
    def test_moves_center(self):
        king = King(self.white, (3, 3))
        rook = Rook(self.white, (4, 4))
        self.board.pieces.add(king)
        self.board.pieces.add(rook)
        moves = list(rook.moves(self.board))
        self.assertEquals(len(moves), 14, moves)

    def test_moves_corner(self):
        king = King(self.white, (3, 3))
        rook = Rook(self.white, (0, 0))
        self.board.pieces.add(king)
        self.board.pieces.add(rook)
        moves = list(rook.moves(self.board))
        self.assertEquals(len(moves), 14, moves)

    def test_moves_blocked_ally(self):
        rook = Rook(self.white, (0, 0))
        king = King(self.white, (0, 1))
        self.board.pieces.add(rook)
        self.board.pieces.add(king)
        moves = list(rook.moves(self.board))
        self.assertEquals(len(moves), 7, moves)

    def test_moves_blocked_enemy(self):
        rook = Rook(self.white, (0, 0))
        knight = Knight(self.black, (0, 1))
        self.board.pieces.add(rook)
        self.board.pieces.add(knight)
        moves = list(rook.moves(self.board))
        self.assertEquals(len(moves), 8, moves)


class BishopTest(ChessTest):
    def test_moves_center(self):
        bishop = Bishop(self.white, (4, 4))
        self.board.pieces.add(bishop)
        moves = list(bishop.moves(self.board))
        self.assertEquals(len(moves), 13, moves)

    def test_moves_corner(self):
        bishop = Bishop(self.white, (0, 0))
        self.board.pieces.add(bishop)
        moves = list(bishop.moves(self.board))
        self.assertEquals(len(moves), 7, moves)

    def test_moves_blocked_ally(self):
        bishop = Bishop(self.white, (0, 0))
        knight = Knight(self.white, (1, 1))
        self.board.pieces.add(bishop)
        self.board.pieces.add(knight)
        moves = list(bishop.moves(self.board))
        self.assertEquals(len(moves), 0, moves)

    def test_moves_blocked_enemy(self):
        bishop = Bishop(self.white, (0, 0))
        knight = Knight(self.black, (1, 1))
        self.board.pieces.add(bishop)
        self.board.pieces.add(knight)
        moves = list(bishop.moves(self.board))
        self.assertEquals(len(moves), 1, moves)


class QueenTest(ChessTest):
    def test_moves_center(self):
        queen = Queen(self.white, (4, 4))
        self.board.pieces.add(queen)
        moves = [_ for _ in queen.moves(self.board)]
        self.assertEquals(len(moves), 13 + 14, moves)

    def test_moves_corner(self):
        queen = Queen(self.white, (0, 0))
        self.board.pieces.add(queen)
        moves = [_ for _ in queen.moves(self.board)]
        self.assertEquals(len(moves), 21, moves)

    def test_moves_blocked_ally(self):
        queen = Queen(self.white, (0, 0))
        king = King(self.white, (1, 1))
        self.board.pieces.add(queen)
        self.board.pieces.add(king)
        moves = [_ for _ in queen.moves(self.board)]
        self.assertEquals(len(moves), 14, moves)

    def test_moves_blocked_enemy(self):
        queen = Queen(self.white, (0, 0))
        king = King(self.black, (1, 1))
        self.board.pieces.add(queen)
        self.board.pieces.add(king)
        moves = [_ for _ in queen.moves(self.board)]
        self.assertEquals(len(moves), 15, moves)


if __name__ == "__main__":
    unittest.main()
