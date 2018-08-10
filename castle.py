import castle

from typing import Tuple


def select_player_types() -> Tuple[castle.PlayerType, castle.PlayerType]:
    player1, player2 = None, None
    while True:
        print(f'1) Play a person')
        print(f'2) Play the computer')
        print(f'3) Play the computer against itself')
        choice_str = input(f'Select an option: ')
        try:
            choice = int(choice_str)
            if choice not in [1, 2, 3]:
                raise ValueError
        except ValueError:
            print('Invalid option.\n')
            continue

        if choice == 1:
            player1 = castle.PlayerType.HUMAN
            player2 = castle.PlayerType.HUMAN
        elif choice == 2:
            player1 = castle.PlayerType.HUMAN
            player2 = castle.PlayerType.COMPUTER
        elif choice == 3:
            player1 = castle.PlayerType.COMPUTER
            player2 = castle.PlayerType.COMPUTER
        break
    return player1, player2


def main():
    print(f'Welcome to castle, a litte chess engine.\n')
    player1, player2 = select_player_types()
    g = castle.Game(player1, player2)
    g.board.pretty_print()
    while True:
        g.play_turn()


if __name__ == '__main__':
    main()
