from typing import List, Tuple
from castle.board import Board, InvalidChessNotationError
from castle.piece import Piece, PieceType, Color
from castle.square import Square


class InvalidMoveError(Exception):
    pass


class MoveParser:
    @staticmethod
    def _find_pawn_for_destination(board: Board, color: Color, dest_square_str: str) -> str:
        dest_square = board.square_from_notation(dest_square_str)
        file = dest_square.file
        # the source square must be in the same file as the destination square
        for square in board.squares_matching_filter(type=PieceType.PAWN, color=color, file=file):
            possible_moves = board.get_moves(square)
            if dest_square in possible_moves:
                return square.notation()
        raise InvalidMoveError(dest_square_str)

    @staticmethod
    def parse_move(board: Board, active_color: Color, move: str) -> Tuple[Square, Square]:
        """Parses chess notation in the context of the board, and returns the piece which is moving and its destination.
        """
        def squares_from_strings(from_notation: str, to_notation: str):
            return board.square_from_notation(from_notation), board.square_from_notation(to_notation)

        # is it a capture? SxDD
        if 'x' in move:
            from_square = move[:move.find('x')]
            to_square = move[move.find('x')+1:]
            print(f'Capture from {from_square} to {to_square}')

            # if this is a pawn capture, the from_square will only be the file that the pawn came from
            if len(from_square) == 1:
                from_square = MoveParser._find_pawn_for_destination(board, active_color, to_square)
            else:
                raise RuntimeError('non-pawn capture')
            return squares_from_strings(from_square, to_square)

        # is it a pawn move? Pawn moves are only 2 characters long. DD
        if len(move) == 2:
            to_square = move
            from_square = MoveParser._find_pawn_for_destination(board, active_color, to_square)
            return squares_from_strings(from_square, to_square)

        # piece type will be the first character
        piece_type = PieceType.type_from_symbol(move[0])
        dest_square = board.square_from_notation(move[1:])
        for square in board.squares_matching_filter(type=piece_type, color=active_color):
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
                self.current_color = Color.WHITE if self.current_color == Color.BLACK else Color.BLACK
            except InvalidMoveError:
                print('Invalid move.')
            except InvalidChessNotationError:
                print('Invalid notation.')
            break

    def player_move(self):
        # XXX(PT): for now, a turn always simply consists of performing a move from stdin
        player_move_str = input(f'{self.current_color.name}\'s move: ')
        from_square, dest_square = MoveParser.parse_move(self.board, self.current_color, player_move_str)
        self.board.move_piece_to_square(from_square, dest_square)

        # XXX(PT): for now, a turn always simply consists of performing a move from stdin
        player_move_str = input('Enter a move: ')
        # XXX(PT): this should later be refactored into a separate step for parsing once it's fleshed out
        # check if they're moving a pawn or a named piece
        if player_move_str[0].islower():
            destination = self.board.square_from_notation(player_move_str)
            # player must be moving a pawn
            # loop through every pawn and see if it's possible for it to move to the specified position
            for square in self.board.squares_occupied_of_type(PieceType.PAWN, self.current_color):
                possible_moves = self.board.get_moves(square)
                print(f'Possible {square} {PieceType.PAWN.name} moves: {possible_moves}')
                if destination in possible_moves:
                    # make a move!
                    self.board.move_piece_to_square(square, destination)
                    return
        else:
            piece_type = PieceType.type_from_symbol(player_move_str[0])
            destination_str = player_move_str[1:]
            destination = self.board.square_from_notation(destination_str)
            for square in self.board.squares_occupied_of_type(piece_type, self.current_color):
                possible_moves = self.board.get_moves(square)
                print(f'Possible {square} {piece_type.name} moves: {possible_moves}')
                if destination in possible_moves:
                    self.board.move_piece_to_square(square, destination)
                    return
        raise InvalidMoveError(player_move_str)
