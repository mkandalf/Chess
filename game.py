from piece import Pawn, Bishop, Knight, Rook, Queen, King
from player import Player, Color
from position import Position


class Game(object):
    def __init__(self, board,
            players=(Player(Color.WHITE), Player(Color.BLACK))):
        self.moves = []
        self.board = board
        self.players = players

    @property
    def ply(self):
        return len(self.moves)

    @property
    def current_player(self):
        """The player whose turn it is."""
        return self.players[self.ply % 2]

    def make_move(self, move):
        """Apply the given move to the board."""
        #Handle castling
        if type(move.piece) == King:
            dy = move.to[0] - move.start[0]
            if abs(dy) == 2:
                if dy == 2:
                    rook = self.board.piece_at((7, move.to[1]))
                    assert rook is not None, (move.piece, self.board.pieces)
                    rook.location = (5, move.to[1])
                else:
                    rook = self.board.piece_at((0, move.to[1]))
                    assert rook is not None, (move.piece, self.board.pieces)
                    rook.location = (3, move.to[1])
            move.piece.owner.castling.append((False, False))
        #Remove castling rights on rook moves
        elif type(move.piece) == Rook:
            if move.start[0] == 0:
                move.piece.owner.castling.append(
                        (False, move.piece.owner.castling[-1][1]))
            if move.start[0] == 7:
                move.piece.owner.castling.append(
                        (move.piece.owner.castling[-1][0], False))
            else:
                move.piece.owner.castling.append(move.piece.owner.castling[-1])
        #Otherwise repeat the last set of castling rights
        else:
            move.piece.owner.castling.append(move.piece.owner.castling[-1])

        if type(move.piece) == Pawn:
            pawn = move.piece
            pawn.just_moved = (pawn.y == pawn.start_rank)

        if move.captured is not None:
            assert move.captured in self.board.pieces, move
            self.board.pieces.remove(move.captured)
        move.piece.location = move.to

        if move.promotion is not None:
            promoted = move.promotion(move.piece.owner, move.piece.location)
            assert move.piece in self.board.pieces
            self.board.pieces.remove(move.piece)
            self.board.pieces.add(promoted)

        self.moves.append(move)

    def undo_move(self):
        """Apply the move in reverse to the board."""
        # restore castling rights
        move = self.moves.pop()

        move.piece.owner.castling.pop()

        # if move was a castle, restore rook position
        if type(move.piece) == King:
            dy = move.to[0] - move.start[0]
            if dy == 2:
                rook = self.board.piece_at((5, move.to[1]))
                rook.location = (7, move.to[1])
                print rook.location
            elif dy == -2:
                rook = self.board.piece_at((3, move.to[1]))
                rook.location = (0, move.to[1])

        # restore piece location
        move.piece.location = move.start
        # restore captured piece
        if move.captured is not None:
            self.board.pieces.add(move.captured)

        # remove promoted piece
        # restore promoting pawn
        if move.promotion is not None:
            promoted = move.promotion(move.piece.owner, move.to)
            assert any(piece == promoted for piece in self.board.pieces), (promoted, self.board.pieces)
            for piece in self.board.pieces:
                if piece == promoted:
                    self.board.pieces.remove(piece)
                    break
            self.board.pieces.add(move.piece)

    def is_legal(self, move):
        """Check if a move is legal.
        A move is legal if
        * a piece can reach the target square
        * an allied piece is not on the target square
        * moving would not place the owner in check."""
        if move.piece.can_reach(self.board, move.to):
            piece = self.board.piece_at(move.to)
            if piece is None or piece.owner != move.piece.owner:
                # disallow castling through check
                if type(move.piece) == King:
                    dx = move.to[0] - move.start[0]
                    if abs(dx) == 2:  # castle
                        through = move.start[0] + dx / 2, move.to[1]
                        if any(piece.can_attack(self.board, through)
                                for piece in self.board.pieces
                                if piece.owner != move.piece.owner):
                            return False

                with Position(self, move) as position:
                    return not move.piece.owner.is_in_check(position)
            else:
                return False
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
        self.board.pieces = set()
        components = fen.split(" ")
        rows = components[0].split("/")
        for row, row_str in enumerate(rows):
            column = 0
            for entry in row_str:
                if entry.isdigit():
                    column += int(entry)
                else:
                    sq = (column, 7 - row)
                    player = self.players[not entry.islower()]
                    entry = entry.lower()
                    if entry.lower() == "r":
                        self.board.pieces.add(Rook(player, sq))
                    elif entry.lower() == "n":
                        self.board.pieces.add(Knight(player, sq))
                    elif entry.lower() == "b":
                        self.board.pieces.add(Bishop(player, sq))
                    elif entry.lower() == "q":
                        self.board.pieces.add(Queen(player, sq))
                    elif entry.lower() == "k":
                        self.board.pieces.add(King(player, sq))
                    elif entry.lower() == "p":
                        self.board.pieces.add(Pawn(player, sq))
                    column += 1
        # self.ply = int(components[1] == "b") + int(components[5]) - 1

    def play(self):
        """Play the game."""
        print "Starting game."
        print "Press CTRL+C to quit."
        print self.board
        while not self.is_over:
            print "%s's turn." % self.current_player
            move = self.current_player.get_move(self.board)
            print move
            if self.is_legal(move):
                self.make_move(move)
                print self.board
            else:
                print "Illegal move."
        if self.is_checkmate(self.current_player):
            print "Checkmate."
        else:
            print "Stalemate"
        print "Game over."
