from .game import Game
from .player import PlayerType
from .piece import PieceType, Piece
from .piece import Color
from .square import Square
import re
from typing import Optional, List


class ParseError(Exception):
    pass


class EndOfStream(Exception):
    pass


class Parser:
    def __init__(self, contents: str):
        self.contents = contents
        self._tokens = self._split_stream(self.contents)
        self._token_index = 0

    def peek_tok(self) -> Optional[str]:
        """Return the next token in the parse stream, without consuming it
        """
        if self._token_index >= len(self._tokens):
            raise EndOfStream
        return self._tokens[self._token_index]

    def _peek_2(self) -> str:
        """Return the token after the next one in the token stream

        Needed for rare cases where we need 2-token lookahead
        For example, this is used to tell if the next line contains '#', 'define', in which case the whole line should
        be ignored.
        """
        return self._tokens[self._token_index+1]

    def get_tok(self) -> str:
        """Return and consume the next token in the parse stream
        """
        tok = self.peek_tok()
        self._token_index += 1
        return tok

    def _enqueue_tok(self, tok: str):
        """Place a token at the top of the queue, so it is next to be read
        """
        self._tokens.insert(self._token_index, tok)

    def match(self, expected: str):
        """Consume the next token, and verify it matches an expected value
        This method will throw a ParseError if the next token did not match the expected value
        """
        real_tok = self.get_tok()
        if real_tok != expected:
            raise ParseError('Expected token {}, got {}'.format(repr(expected), repr(real_tok)))

    @staticmethod
    def _split_stream(stream: str) -> List[str]:
        return list(stream)

    def match_str(self, expected: str) -> None:
        """Given a source string, tokenize it and ensure the token stream matches those tokens exactly.
        Also consumes the tokens.
        """
        expected_stream = self._split_stream(expected)
        for expected_tok in expected_stream:
            try:
                self.match(expected_tok)
            except ParseError:
                raise ParseError(f'Matching string {expected_stream} failed!')

    def read_to(self, expected: str, include_delim=False) -> List[str]:
        """Read tokens up to and including the next instance of 'expected'

        Returns the tokens read up to and including 'expected'
        """
        return self.read_to_any([expected], include_delim)

    def read_to_any(self, possibilities: List[str], include_delim=False) -> List[str]:
        """Read tokens up to and including the next instance of any element in 'possibilities'

        Returns the tokens read up to and including the matched possibility
        """
        tokens_read: List[str] = []
        while True:
            tok = self.get_tok()
            if tok in possibilities:
                if include_delim:
                    tokens_read.append(tok)
                break

            tokens_read.append(tok)
        return tokens_read


class FenGameConstructor:
    """Parses a FEN move string and returns the corresponding Game
    """
    # FEN := PiecePlacement
    #     += ' ' Side to move
    #     += ' ' Castling ability
    #     += ' ' En passant target square
    #     += ' ' Halfmove clock
    #     += ' ' Fullmove counter
    # <digit19> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
    # <digit>   ::= '0' | <digit19>

    def __init__(self, game_state: str):
        self.parser = Parser(game_state)
        self.game: Game = None
        self.parse_game()

    def parse_game(self):
        self.game = Game(PlayerType.HUMAN, PlayerType.HUMAN)
        self.game.board.clear()

        self.parse_piece_placement()
        self.parse_side_to_move()
        self.parse_castling_ability()
        self.parse_en_passant_target_square()
        # optional
        try:
            self.parse_fullmove_counter()
            self.parse_halfmove_clock()
        except EndOfStream:
            pass

    # <Piece Placement> ::= <rank8>'/'<rank7>'/'<rank6>'/'<rank5>'/'<rank4>'/'<rank3>'/'<rank2>'/'<rank1>
    # <rank>       ::= [<digit17>]<piece> {[<digit17>]<piece>} [<digit17>] | '8'
    # <piece>       ::= <white Piece> | <black Piece>
    # <digit17>     ::= '1' | '2' | '3' | '4' | '5' | '6' | '7'
    # <white Piece> ::= 'P' | 'N' | 'B' | 'R' | 'Q' | 'K'
    # <black Piece> ::= 'p' | 'n' | 'b' | 'r' | 'q' | 'k'
    def parse_piece_placement(self):
        def piece_from_symbol(symbol: str) -> Piece:
            color = Color.WHITE if symbol.isupper() else Color.BLACK
            piece_type = PieceType.type_from_symbol(symbol.upper())
            return Piece(piece_type, color)

        for rank in range(7, -1, -1):
            file = 0
            while file < 8:
                tok = self.parser.get_tok()
                if tok.isdigit():
                    # some number of empty squares
                    file += int(tok)
                    continue
                else:
                    piece = piece_from_symbol(tok)
                    file_str = Square.index_to_file(file)
                    self.game.board.place_piece(piece, f'{file_str}{rank+1}')
                file += 1
            if rank == 0:
                self.parser.match(' ')
            else:
                self.parser.match('/')
        self.game.board.pretty_print()

    # <Side to move> ::= {'w' | 'b'}
    def parse_side_to_move(self):
        player = self.parser.get_tok()
        if player == 'w':
            self.game.set_color_to_move(Color.WHITE)
        else:
            self.game.set_color_to_move(Color.BLACK)
        self.parser.match(' ')

    # <Castling ability> ::= '-' | ['K'] ['Q'] ['k'] ['q'] (1..4)
    def parse_castling_ability(self):
        castling_data = self.parser.read_to(' ', include_delim=True)
        if castling_data[0] == '-':
            # no castling possible
            # TODO(PT): test this
            self.game.can_white_castle_short = False
            self.game.can_white_castle_long = False
            self.game.can_black_castle_short = False
            self.game.can_black_castle_long = False
            return
        # trim space at the end
        for c in castling_data[:-1]:
            color = Color.WHITE if c.isupper() else Color.BLACK
            short = c.upper() == 'K'
            if color == Color.WHITE:
                if short:
                    self.game.can_white_castle_short = True
                else:
                    self.game.can_white_castle_long = True
            else:
                if short:
                    self.game.can_black_castle_short = True
                else:
                    self.game.can_black_castle_long = True

    # <En passant target square> ::= '-' | <epsquare>
    # <epsquare>   ::= <fileLetter> <eprank>
    # <fileLetter> ::= 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h'
    # <eprank>     ::= '3' | '6'
    def parse_en_passant_target_square(self):
        if self.parser.peek_tok() == '-':
            self.parser.match('-')
            return

        target = self.parser.read_to(' ')
        self.game.en_passant_target_square = self.game.board.square_from_notation(target)

    # <Fullmove counter> ::= <digit19> {<digit>}
    def parse_fullmove_counter(self):
        move = self.parser.read_to(' ', include_delim=True)[:-1]
        move = ''.join(move)
        print(f'FEN parser: fullmove {move}')

    # <Halfmove Clock> ::= <digit> {<digit>}
    # <digit> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
    def parse_halfmove_clock(self):
        halfmove_clock = ''
        while True:
            try:
                halfmove_char = self.parser.get_tok()
                halfmove_clock += halfmove_char
            except EndOfStream:
                break
        print(f'FEN parser: halfmove {halfmove_clock}')
