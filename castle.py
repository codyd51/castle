import castle


def main():
    b = castle.Board()
    print(b.square_from_notation('a3'))
    print(b.square_from_notation('jr'))
    print(b.square_from_notation('a3'))


if __name__ == '__main__':
    main()
