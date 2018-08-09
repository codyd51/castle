from typing import List
from castle.board import Board, InvalidChessNotationError
from castle.piece import Piece, PieceType, Color
from castle.player import HumanPlayer, RandomPlayer
from castle.move import Move, MoveParser, InvalidMoveError


class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.moves: List[Move] = []

        self.white_player = HumanPlayer(Color.WHITE)
        self.black_player = RandomPlayer(Color.BLACK)
        self.current_player = self.white_player

        self.place_pieces_for_new_game()

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
        for i in range(3):
            try:
                move = self.current_player.play_move(self.board)
                if type(move) == str:
                    self.apply_notation(move)
                elif type(move) == Move:
                    self.apply_move(move)
                else:
                    raise RuntimeError(f'unknown move type {type(move)}')
                self.pretty_print()
                return
            except InvalidMoveError as e:
                stripped_notation = str(e).strip('P')
                print(f'Invalid move. {stripped_notation}.')
            except InvalidChessNotationError as e:
                stripped_notation = str(e).strip('P')
                print(f'Invalid notation. {stripped_notation}.')
        raise RuntimeError(f'{self.current_player.color.name} provided invalid move 3 times.')

    def apply_notation(self, move_str: str) -> None:
        move = MoveParser.parse_move(self.board, self.current_player.color, move_str)
        self.apply_move(move)

    def apply_move(self, move: Move) -> None:
        self.board.move_piece_to_square(move.from_square, move.to_square)
        self.moves.append(move)
        self.current_player = self.white_player if self.current_player == self.black_player else self.black_player

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
