from board import Board
from piece import Pawn, Bishop, Knight, Rook, Queen, King
from player import Player, Color
from position import Position


class Game(object):
    def __init__(self, board,
            players=(Player(Color.WHITE), Player(Color.BLACK))):
        self.moves = []
        self.board = board
        self.players = players
        self.ply = 0

    @property
    def current_player(self):
        """The player whose turn it is."""
        return self.players[self.ply % 2]

    def _make_move(self, move):
        """Apply the given move to the board."""
        #Handle castling
        if type(move.piece) == King:
            dy = move.to[0] - move.start[0]
            if abs(dy) == 2:
                if dy == 2:
                    rook = self.board.piece_at((7, move.to[1]))
                    assert rook is not None, (move.piece, self.board._pieces)
                    self.board.move_piece(rook, (5, move.to[1]))
                else:
                    rook = self.board.piece_at((0, move.to[1]))
                    assert rook is not None, (move.piece, self.board._pieces)
                    self.board.move_piece(rook, (3, move.to[1]))
            move.piece.owner.castling.append((False, False))
        #Remove castling rights on rook moves
        elif type(move.piece) == Rook:
            if move.start[0] == 0:
                move.piece.owner.castling.append(
                        (False, move.piece.owner.castling[-1][1]))
            elif move.start[0] == 7:
                move.piece.owner.castling.append(
                        (move.piece.owner.castling[-1][0], False))
            else:
                move.piece.owner.castling.append(move.piece.owner.castling[-1])
        #Otherwise repeat the last set of castling rights
        else:
            move.piece.owner.castling.append(move.piece.owner.castling[-1])

        # handle en-passant
        if type(move.piece) == Pawn:
            pawn = move.piece
            pawn.just_moved = (pawn.y == pawn.start_rank)

        if move.captured is not None:
            self.board.remove_piece(move.captured)

        self.board.move_piece(move.piece, move.to)

        if move.promotion is not None:
            promoted = move.promotion(move.piece.owner, move.piece.location)
            self.board.remove_piece(move.piece)
            self.board.add_piece(promoted)

        self.moves.append(move)
        self.ply += 1

    def _undo_move(self):
        """Apply the move in reverse to the board."""
        # restore castling rights
        self.ply -= 1
        move = self.moves.pop()

        move.piece.owner.castling.pop()

        # if move was a castle, restore rook position
        if type(move.piece) == King:
            dy = move.to[0] - move.start[0]
            if dy == 2:
                rook = self.board.piece_at((5, move.to[1]))
                self.board.move_piece(rook, (7, move.to[1]))
            elif dy == -2:
                rook = self.board.piece_at((3, move.to[1]))
                self.board.move_piece(rook, (0, move.to[1]))

        # remove promoted piece
        # restore promoting pawn
        if move.promotion is not None:
            promoted = move.promotion(move.piece.owner, move.to)
            self.board.remove_piece(promoted)
            self.board.add_piece(move.piece)

        # restore piece location
        self.board.move_piece(move.piece, move.start)

        # restore captured piece
        if move.captured is not None:
            self.board.add_piece(move.captured)

    def is_legal(self, move):
        """Check if a move is legal.
        A move is legal if
        * a piece can reach the target square
        * an allied piece is not on the target square
        * moving would not place the owner in check."""
        piece = self.board.piece_at(move.to)
        if piece is None or piece.owner != move.piece.owner:
            # disallow castling through check
            if type(move.piece) == King:
                dx = move.to[0] - move.start[0]
                if abs(dx) == 2:  # castle
                    through = move.start[0] + dx / 2, move.to[1]
                    if any((piece.can_attack(self.board, through) or 
                            piece.can_attack(self.board, move.start))
                            for piece in self.board.pieces
                            if piece.owner != move.piece.owner):
                        return False

            with Position(self, move) as position:
                return not move.piece.owner.is_in_check(position)
        else:
            return False

    @property
    def is_over(self):
        """Check if the game is over for the given player.
        The game is over if a player cannot make any moves."""
        return not any(self.is_legal(move)
                for move in self.current_player.moves(self.board))

    def is_checkmate(self, player):
        """Check if the given player is checkmated.
        A player is checkmated if the game is over
        and the player is in check."""
        return self.is_over and player.is_in_check(self.board)

    def is_stalemate(self, player):
        """Check if the given player is stalemated.
        A player is stalemated if the game is over
        and the player is not in check."""
        return self.is_over and not player.is_in_check(self.board)

    def from_fen(self, fen):
        """Reset game to match given FEN string"""
        self.board = Board()
        components = fen.split(" ")
        rows = components[0].split("/")
        for row, row_str in enumerate(rows):
            column = 0
            for entry in row_str:
                if entry.isdigit():
                    column += int(entry)
                else:
                    sq = (column, 7 - row)
                    player = self.players[entry.islower()]
                    entry = entry.lower()
                    if entry.lower() == "r":
                        self.board.add_piece(Rook(player, sq))
                    elif entry.lower() == "n":
                        self.board.add_piece(Knight(player, sq))
                    elif entry.lower() == "b":
                        self.board.add_piece(Bishop(player, sq))
                    elif entry.lower() == "q":
                        self.board.add_piece(Queen(player, sq))
                    elif entry.lower() == "k":
                        self.board.add_piece(King(player, sq))
                    elif entry.lower() == "p":
                        self.board.add_piece(Pawn(player, sq))
                    column += 1
        # self.ply = int(components[1] == "b") + int(components[5]) - 1

    def play(self):
        """Play the game."""
        print "Starting game."
        print "Press CTRL+C to quit."
        print self.board
        while not self.is_over:
            print "%s's turn." % self.current_player
            move = self.current_player.get_move(self)
            print move
            if self.is_legal(move):
                self._make_move(move)
                print self.board
            else:
                print "Illegal move."
        if self.is_checkmate(self.current_player):
            print "Checkmate."
        else:
            print "Stalemate"
        print "Game over."

    def perft(self, depth):
        nodes = 0
        for move in self.current_player.moves(self.board):
            if self.is_legal(move):
                if (depth == 1):
                    nodes += 1
                else:
                    self._make_move(move)
                    nodes += self.perft(depth - 1)
                    self._undo_move()
        return nodes

    def perft_captures(self, depth):
        nodes = 0
        for move in self.current_player.moves(self.board):
            if self.is_legal(move):
                if (depth == 1):
                    if (move.captured):
                        nodes += 1
                else:
                    self._make_move(move)
                    nodes += self.perft_captures(depth - 1)
                    self._undo_move()
        return nodes

    def divide(self, depth):
        print self.board
        if (depth == 1):
            for move in self.current_player.moves(self.board):
                if self.is_legal(move):
                    self._make_move(move)
                    print move
                    self._undo_move()
        else:
            for move in self.current_player.moves(self.board):
                if self.is_legal(move):
                    self._make_move(move)
                    print move, " ", self.perft(depth-1)
                    self._undo_move()
