import logging
from enum import Enum
from typing import List, Optional, Set

from castle.board import Board, InvalidChessNotationError
from castle.piece import Piece, PieceType, Color
from castle.player import HumanPlayer, RandomPlayer
from castle.move import Move, CastleMove, MoveParser, InvalidMoveError
from castle.player import PlayerType
from castle.square import Square


class Winner(Enum):
    DRAW = 0
    WHITE = 1
    BLACK = 2

    @classmethod
    def from_color(cls, color: Color):
        if color == Color.WHITE:
            return Winner.WHITE
        elif color == Color.BLACK:
            return Winner.BLACK
        raise RuntimeError(f'No conversion from {color} to Winner')


class Game:
    def __init__(self, player1: PlayerType, player2: PlayerType) -> None:
        self.board = Board()
        self.moves: List[Move] = []
        self.place_pieces_for_new_game()

        self.finished = False
        self.winner: Optional[Winner] = None

        if player1 == PlayerType.HUMAN:
            self.white_player = HumanPlayer(Color.WHITE)
        else:
            self.white_player = RandomPlayer(Color.WHITE)
        if player2 == PlayerType.HUMAN:
            self.black_player = HumanPlayer(Color.BLACK)
        else:
            self.black_player = RandomPlayer(Color.BLACK)
        self.current_player = self.white_player

    def place_pieces_for_new_game(self) -> None:
        # white's pieces
        self.board.place_piece(Piece(PieceType.ROOK, Color.WHITE), 'a1')
        self.board.place_piece(Piece(PieceType.KNIGHT, Color.WHITE), 'b1')
        self.board.place_piece(Piece(PieceType.BISHOP, Color.WHITE), 'c1')
        self.board.place_piece(Piece(PieceType.QUEEN, Color.WHITE), 'd1')
        self.board.place_piece(Piece(PieceType.KING, Color.WHITE), 'e1')
        self.board.place_piece(Piece(PieceType.BISHOP, Color.WHITE), 'f1')
        self.board.place_piece(Piece(PieceType.KNIGHT, Color.WHITE), 'g1')
        self.board.place_piece(Piece(PieceType.ROOK, Color.WHITE), 'h1')
        self.board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'a2')
        self.board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'b2')
        self.board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'c2')
        self.board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'd2')
        self.board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'e2')
        self.board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'f2')
        self.board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'g2')
        self.board.place_piece(Piece(PieceType.PAWN, Color.WHITE), 'h2')

        # black's pieces
        self.board.place_piece(Piece(PieceType.ROOK, Color.BLACK), 'a8')
        self.board.place_piece(Piece(PieceType.KNIGHT, Color.BLACK), 'b8')
        self.board.place_piece(Piece(PieceType.BISHOP, Color.BLACK), 'c8')
        self.board.place_piece(Piece(PieceType.QUEEN, Color.BLACK), 'd8')
        self.board.place_piece(Piece(PieceType.KING, Color.BLACK), 'e8')
        self.board.place_piece(Piece(PieceType.BISHOP, Color.BLACK), 'f8')
        self.board.place_piece(Piece(PieceType.KNIGHT, Color.BLACK), 'g8')
        self.board.place_piece(Piece(PieceType.ROOK, Color.BLACK), 'h8')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'a7')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'b7')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'c7')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'd7')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'e7')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'f7')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'g7')
        self.board.place_piece(Piece(PieceType.PAWN, Color.BLACK), 'h7')

    def play_turn(self) -> None:
        for i in range(5):
            try:
                move = self.current_player.play_move(self.board)
                legal_moves = self.get_all_legal_moves(self.current_player.color)
                if move not in legal_moves:
                    raise InvalidMoveError('Illegal')

                self.apply_move(move)
                self.pretty_print()
                return
            except InvalidMoveError as e:
                stripped_notation = str(e).strip('P')
                print(f'Invalid move. {stripped_notation}.')
            except InvalidChessNotationError as e:
                stripped_notation = str(e).strip('P')
                print(f'Invalid notation. {stripped_notation}.')
        raise RuntimeError(f'{self.current_player.color.name} provided invalid move 3 times.')

    def get_all_legal_moves(self, color: Color) -> Set[Move]:
        """Returns a set of all legal Moves from the current board state, respecting rules like check.
        This method does 'move post processing' to transform a pseudo-legal
        """
        all_moves = self.board.get_all_moves(color)
        legal_moves = all_moves.copy()
        # restrict moves to ones that do not result in the player being in check after this turn
        for move in all_moves:
            if self.board.board_after_move(move).is_in_check(color):
                # throw this move away because it results in us being in check
                legal_moves.remove(move)

        # add in castle moves if possible
        for on_kingside in [True, False]:
            if self.can_castle(color, on_kingside):
                side = 'kingside' if on_kingside else 'queenside'
                logging.debug(f'{color} can {side} castle')
                legal_moves.add(CastleMove(color, on_kingside))

        return legal_moves

    def can_castle(self, color: Color, kingside: bool):
        # have they already castled?
        if len(list(self.moves_matching_filter(color=color, is_castle=True))):
            return False
        # have they moved their king?
        if len(list(self.moves_matching_filter(color=color, from_type=PieceType.KING))):
            return False
        # have they moved their rook?
        rook_file = 0 if kingside else 7
        rook_rank = 7 if kingside else 0
        rook_square = self.board.square_from_coord(rook_rank, rook_file)
        if len(list(self.moves_matching_filter(color=color, from_square=rook_square))):
            return False

        # are they in check?
        if self.board.is_in_check(color):
            return False

        if color == Color.WHITE:
            if kingside:
                traveled_square_notations = ['f1', 'g1']
            else:
                traveled_square_notations = ['d1', 'c1', 'b1']
            king_square = self.board.square_from_notation('e1')
        else:
            if kingside:
                traveled_square_notations = ['f8', 'g8']
            else:
                traveled_square_notations = ['d8', 'c8', 'b8']
            king_square = self.board.square_from_notation('e8')
        traveled_squares = [self.board.square_from_notation(x) for x in traveled_square_notations]

        # are any of the squares in the way obstructed?
        for s in traveled_squares:
            if s.occupant:
                return False

        # would moving on any of the squares on the way put the king in check?
        for s in traveled_squares:
            move = MoveParser.move_from_squares(king_square, s)
            if self.board.board_after_move(move).is_in_check(color):
                return False

        # would castling put the player in check?
        if self.board.board_after_move(CastleMove(color, kingside)).is_in_check(color):
            return False

        return True

    def apply_notation(self, move_str: str) -> None:
        move = MoveParser.parse_move(self.board, self.current_player.color, move_str)
        self.apply_move(move)

    def swap_player(self):
        self.current_player = self.white_player if self.current_player == self.black_player else self.black_player

    def apply_move(self, move: Move) -> None:
        self.board.apply_move(move)

        # update game state
        self.moves.append(move)
        previous_player = self.current_player
        self.swap_player()

        # endgame detection
        if self.is_in_checkmate(self.current_player.color):
            self.finished = True
            self.winner = Winner.from_color(previous_player.color)
        elif self.is_in_stalemate(self.current_player.color):
            self.finished = True
            self.winner = Winner.DRAW

    def pretty_print(self) -> None:
        self.board.pretty_print()
        it = iter(self.moves)
        turn = 1
        for move1 in it:
            print(f'{turn}. {move1.notation} ', end='')
            try:
                move2 = next(it)
                print(f'{move2.notation} ', end='')
            except StopIteration:
                pass
            turn += 1
        print()

    def winner(self) -> Optional[Color]:
        if self.is_in_checkmate(Color.WHITE):
            return Color.BLACK
        elif self.is_in_checkmate(Color.BLACK):
            return Color.WHITE
        return None

    def undo_move(self):
        if not len(self.moves):
            raise InvalidMoveError('Can\'t undo from starting position')

        # TODO(PT): test me please!
        last_move = self.moves.pop()
        if type(last_move) == CastleMove:
            raise RuntimeError(f'undo castle')

        self.board.move_piece_to_square(last_move.to_square, last_move.from_square)

        # restore the previous occupant of the square, if any
        if last_move.is_capture:
            self.board.place_piece(last_move.captured_piece, last_move.to_square.notation())

        # restore active player
        self.swap_player()

    def perft(self, depth: int) -> int:
        if depth == 0:
            return 1

        moves = self.get_all_legal_moves(self.current_player.color)
        game_states = 0

        for move in moves:
            self.apply_move(move)
            game_states += self.perft(depth - 1)
            self.undo_move()
        return game_states

    def is_in_checkmate(self, color: Color) -> bool:
        """Can the opposite color capture the King on their next turn, and the playing color has no way out of this?
        """
        # TODO(PT): test me
        return self.board.is_in_check(color) and len(self.get_all_legal_moves(color)) == 0

    def is_in_stalemate(self, color: Color) -> bool:
        """Does the King have no legal moves?
        """
        # TODO(PT): test me
        return not self.board.is_in_check(color) and len(self.get_all_legal_moves(color)) == 0

    def moves_matching_filter(self,
                              color: Color = None,
                              from_square: Square = None,
                              to_square: Square = None,
                              from_type: PieceType = None,
                              is_castle: bool = False):
        for move in self.moves:
            if color and move.color != color:
                continue

            if is_castle is not None:
                desired_class = CastleMove if is_castle else Move
                if type(move) != desired_class:
                    continue

            if type(move) != CastleMove:
                if from_square and from_square != move.from_square:
                    continue
                if to_square and to_square != move.to_square:
                    continue
                if from_type and from_type != move.active_piece.type:
                    continue
            yield move
