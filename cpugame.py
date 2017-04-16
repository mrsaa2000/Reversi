import cpu
import reversiCore
from reversiCore import Stone, State, SQ_NUM


class Game(object):

    def __init__(self):
        self.reversi = reversiCore.Reversi()
        self.reversi.state = State.PLAY
        self.level0 = cpu.Level0()
        self.level0.init_cpu(Stone.WHITE)

        while True:
            if self.reversi.state == State.GAMEOVER:
                break

            # black
            if self.reversi.turn == Stone.BLACK:
                self.reversi.cpu.board.board = self.reversi.board.copy()
                y, x = self.reversi.cpu.next_move(self.reversi.cpu.board, Stone.BLACK)
                self.reversi.turn_action(y, x)

            if self.reversi.state == State.GAMEOVER:
                break

            # white
            if self.reversi.turn == Stone.WHITE:
                y, x = self.level0.next_move(self.reversi.board)
                self.reversi.turn_action(y, x)

    def get_winner(self):
        black_score = self.reversi.get_score(Stone.BLACK)
        white_score = self.reversi.get_score(Stone.WHITE)
        if black_score > white_score:
            return 'black'
        elif black_score < white_score:
            return 'white'
        elif black_score == white_score:
            return 'draw'

    def print_board(self):
        print(self.reversi.turn.name)
        for y in range(SQ_NUM):
            for x in range(SQ_NUM):
                if self.reversi.board.board[y][x] == Stone.BLACK:
                    print('●', end='')
                elif self.reversi.board.board[y][x] == Stone.WHITE:
                    print('◯', end='')
                elif self.reversi.board.board[y][x] == Stone.EMPTY:
                    print(' ', end='')

                if x == SQ_NUM - 1:
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
