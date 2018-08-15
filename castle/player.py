import random
from enum import Enum
from typing import Tuple, List, Set, Union

from castle.piece import Color
from castle.board import Board
from castle.square import Square
from castle.move import Move, MoveParser


class PlayerType(Enum):
    HUMAN = 0
    COMPUTER = 1


class Player:
    def __init__(self, color: Color):
        self.color = color
        self.name: str = None

    def play_move(self, board: Board) -> Union[str, Move]:
        print(f'{self.color.name.title()}\'s move ({self.name}): ', end='')
        return ''


class HumanPlayer(Player):
    def __init__(self, color: Color):
        super(HumanPlayer, self).__init__(color)
        self.name = 'Player'

    def play_move(self, board: Board) -> Move:
        super(HumanPlayer, self).play_move(board)
        # human player's move consists of asking the user for a move in chess notation
        player_move_str = input()
        return MoveParser.parse_move(board, self.color, player_move_str)


class RandomPlayer(Player):
    def __init__(self, color: Color):
        super(RandomPlayer, self).__init__(color)
        self.name = 'Computer'

    def play_move(self, board: Board) -> Move:
        super(RandomPlayer, self).play_move(board)
        all_move_sets: List[Tuple[Square, Set[Square]]] = []
        for square in board.squares_matching_filter(color=self.color):
            moves = board.get_moves(square)
            if len(moves):
                all_move_sets.append((square, moves))
        # pick a random piece/move set
        source, moves = random.choice(all_move_sets)
        # then pick a move from that set
        dest = random.sample(moves, 1)[0]

        move = Move(self.color, '')
        move.active_piece = source.occupant
        move.from_square = source
        move.to_square = dest
        if dest.occupant:
            move.is_capture = True
            move.captured_piece = dest.occupant
        notation = MoveParser.notation_from_move(move)
        move.notation = notation

        # output the move as if the computer entered it to the CLI
        print(move.notation)

        return move
