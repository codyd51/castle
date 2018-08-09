import castle


def main():
    g = castle.Game()
    g.board.pretty_print()
    while True:
        g.play_turn()



if __name__ == '__main__':
    main()
