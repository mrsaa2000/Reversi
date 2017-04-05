import reversiCore


class Game(object):

    def __init__(self):
        self.reversi = reversiCore.Reversi()
        self.reversi.state = reversiCore.State.PLAY

        while True:
            if self.reversi.state == reversiCore.State.GAMEOVER:
                break

            # black
            if self.reversi.turn == reversiCore.Stone.BLACK:
                y, x = self.reversi.cpu()
                self.reversi.turn_action(y, x)
            self.print_board()

            if self.reversi.state == reversiCore.State.GAMEOVER:
                break

            # white
            if self.reversi.turn == reversiCore.Stone.WHITE:
                y, x = self.reversi.cpu()
                self.reversi.turn_action(y, x)
            self.print_board()

    def get_winner(self):
        black_score = self.reversi.get_black_score()
        white_score = self.reversi.get_white_score()
        if black_score > white_score:
            return 'black'
        elif black_score < white_score:
            return 'white'
        elif black_score == white_score:
            return 'draw'

    def print_board(self):
        print(self.reversi.turn.name)
        for y in range(reversiCore.SQ_NUM):
            for x in range(reversiCore.SQ_NUM):
                if self.reversi.board[y][x] == reversiCore.Stone.BLACK:
                    print('●', end='')
                elif self.reversi.board[y][x] == reversiCore.Stone.WHITE:
                    print('◯', end='')
                elif self.reversi.board[y][x] == reversiCore.Stone.EMPTY:
                    print(' ', end='')

                if x == reversiCore.SQ_NUM - 1:
                    print()
        print()


def main():
    black_win = 0
    white_win = 0
    draw = 0
    times = 1000  # 試行回数

    for i in range(times):
        print(i)
        game = Game()
        if game.get_winner() == 'black':
            black_win += 1
        elif game.get_winner() == 'white':
            white_win += 1
        elif game.get_winner() == 'draw':
            draw += 1

    print('black:{}, white:{}, draw:{}'.format(black_win, white_win, draw))


if __name__ == '__main__':
    main()
