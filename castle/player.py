from typing import Tuple, List, Set, Union
import random

from castle.piece import Color
from castle.board import Board
from castle.square import Square
from castle.move import Move


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

    def play_move(self, board: Board) -> str:
        super(HumanPlayer, self).play_move(board)
        # human player's move consists of asking the user for a move in chess notation
        player_move_str = input()
        return player_move_str


class RandomPlayer(Player):
    def __init__(self, color: Color):
        super(RandomPlayer, self).__init__(color)
        self.name = 'Computer'

    def play_move(self, board: Board) -> Move:
        super(RandomPlayer, self).play_move(board)
        possible_moves: List[Tuple[Square, Set[Square]]] = []
        for square in board.squares_matching_filter(color=self.color):
            moves = board.get_moves(square)
            if len(moves):
                possible_moves.append((square, moves))
        # pick a random valid move
        source, moves = random.choice(possible_moves)
        dest = random.sample(moves, 1)[0]

        move = Move(self.color, f'({source}->{dest})')
        move.from_square = source
        move.to_square = dest
        # output the move as if the computer entered it to the CLI
        print(move.notation)
        return move
