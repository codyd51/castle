from typing import List, Tuple
from castle.board import Board, InvalidChessNotationError
from castle.piece import Piece, PieceType, Color
from castle.square import Square


class InvalidMoveError(Exception):
    pass


class MoveParser:
    @staticmethod
    def parse_move(board: Board, active_color: Color, move: str) -> Tuple[Square, Square]:
        """Parses chess notation in the context of the board, and returns the piece which is moving and its destination.
        """
        def squares_from_strings(from_notation: str, to_notation: str):
            return board.square_from_notation(from_notation), board.square_from_notation(to_notation)

        # if a pawn is being moved, prepend a P to the notation string so pawn movements are internally
        # consistent with other piece's movement. This is so all pieces can be handled with the same logic.
        if move[0].islower():
            move = f'P{move}'

        # is it a capture? SxDD
        if 'x' in move:
            # TODO(PT): add support for Nexd6
            from_square = move[:move.find('x')]
            to_square_str = move[move.find('x')+1:]
            to_square = board.square_from_notation(to_square_str)
            print(f'Capture from {from_square} to {to_square}')

            from_type = PieceType.type_from_symbol(from_square[0])
            from_squares = list(board.squares_matching_filter(type=from_type,
                                                              color=active_color,
                                                              can_reach_square=to_square))
            # there should be exactly one source square
            if len(from_squares) != 1:
                raise InvalidMoveError(move)
            from_square = from_squares[0].notation()
            return squares_from_strings(from_square, to_square_str)

        # piece type will be the first character
        piece_type = PieceType.type_from_symbol(move[0])
        # if the total move is >= 4 characters, then the second character specifies the file of the source piece (Ned6)
        if len(move) >= 4:
            from_file = move[1]
            dest_square = board.square_from_notation(move[2:])
        else:
            from_file = None
            dest_square = board.square_from_notation(move[1:])

        pieces_fulfilling_source_square_requirements: List[Square] = []
        for square in board.squares_matching_filter(type=piece_type, color=active_color, file_str=from_file):
            moves = board.get_moves(square)
            if dest_square in moves:
                # found the piece to move
                return squares_from_strings(square.notation(), dest_square.notation())

        raise RuntimeError(f'{active_color.name} can\'t perform {move}')


class Game:
    def __init__(self):
        self.board = Board()
        self.pieces: List[Piece] = None
        self.place_pieces_for_new_game()
        self.current_color = Color.WHITE

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
            except InvalidMoveError as e:
                print(f'Invalid move. {str(e)}.')
            except InvalidChessNotationError as e:
                print(f'Invalid notation. {str(e)}.')
            break

    def player_move(self):
        # XXX(PT): for now, a turn always simply consists of performing a move from stdin
        player_move_str = input(f'{self.current_color.name}\'s move: ')
        self.apply_move(player_move_str)

    def apply_move(self, move: str):
        from_square, dest_square = MoveParser.parse_move(self.board, self.current_color, move)
        self.board.move_piece_to_square(from_square, dest_square)
        self.current_color = Color.WHITE if self.current_color == Color.BLACK else Color.BLACK
