from typing import List
from castle.board import Board, InvalidChessNotationError
from castle.piece import Piece, PieceType, Color
from castle.player import HumanPlayer, RandomPlayer
from castle.move import Move, MoveParser, InvalidMoveError


class Game:
    def __init__(self):
        self.board = Board()
        self.pieces: List[Piece] = None
        self.place_pieces_for_new_game()
        self.current_color = Color.WHITE

        self.moves: List[Move] = []

    def place_pieces_for_new_game(self):
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

    def play_turn(self):
        while True:
            try:
                self.player_move()
                self.pretty_print()
            except InvalidMoveError as e:
                stripped_notation = str(e).strip('P')
                print(f'Invalid move. {stripped_notation}.')
            except InvalidChessNotationError as e:
                stripped_notation = str(e).strip('P')
                print(f'Invalid notation. {stripped_notation}.')
            break

    def player_move(self):
        # XXX(PT): for now, a turn always simply consists of performing a move from stdin
        player_move_str = input(f'{self.current_color.name.title()}\'s move: ')
        self.apply_move(player_move_str)

    def apply_move(self, move_str: str):
        move = MoveParser.parse_move(self.board, self.current_color, move_str)
        self.board.move_piece_to_square(move.from_square, move.to_square)
        self.current_color = Color.WHITE if self.current_color == Color.BLACK else Color.BLACK
        self.moves.append(move)

    def pretty_print(self):
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
