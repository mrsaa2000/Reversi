import enum
import random


SQ_NUM = 8  # COL,ROWの数
State = enum.Enum('State', 'PLAY GAMEOVER')
Stone = enum.Enum('Stone', 'EMPTY BLACK WHITE')


class Reversi(object):

    def __init__(self):
        self.board = [[Stone.EMPTY for x in range(SQ_NUM)] for y in range(SQ_NUM)]
        self.state = State.PLAY
        self.turn = Stone.BLACK
        self.cpu_player = Stone.WHITE
        self.init_game()

    def change_turn(self):
        self.turn = self.get_enemy()
        if self.is_pass():
            self.turn = self.get_enemy()

    def check_gameover(self):
        for y in range(SQ_NUM):
            for x in range(SQ_NUM):
                if self.board[y][x] == Stone.EMPTY:
                    return
        self.state = State.GAMEOVER

    def cpu(self):
        putable_points = self.get_putable_points()
        y, x = putable_points[random.randint(0, len(putable_points) - 1)]
        self.turn_action(y, x)

    def flip_board(self, y, x, directions):
        """
        指定された座標からひっくり返すことができる石を
        全てひっくり返す
        """
        for direction in directions:
            self.flip_line(y, x, direction)

    def flip_line(self, y, x, direction):
        """
        指定された座標から一方向へ石をひっくり返す
        """
        dy, dx = direction
        ny, nx = y + dy, x + dx
        while True:
            if self.board[ny][nx] == self.turn:
                break
            self.board[ny][nx] = self.turn
            ny, nx = ny + dy, nx + dx

    def get_enemy(self):
        enemy = None
        if self.turn == Stone.BLACK:
            enemy = Stone.WHITE
        else:
            enemy = Stone.BLACK
        return enemy

    def get_putable_points(self):
        points = []
        for y in range(SQ_NUM):
            for x in range(SQ_NUM):
                if self.is_put(y, x):
                    points.append((y, x))
        return points

    def get_black_score(self):
        count = 0
        for y in range(SQ_NUM):
            for x in range(SQ_NUM):
                if self.board[y][x] == Stone.BLACK:
                    count += 1
        return count

    def get_white_score(self):
        count = 0
        for y in range(SQ_NUM):
            for x in range(SQ_NUM):
                if self.board[y][x] == Stone.WHITE:
                    count += 1
        return count

    def init_game(self):
        self.board = [[Stone.EMPTY for x in range(SQ_NUM)] for y in range(SQ_NUM)]
        self.board[SQ_NUM // 2 - 1][SQ_NUM // 2 - 1] = Stone.WHITE
        self.board[SQ_NUM // 2 - 1][SQ_NUM // 2] = Stone.BLACK
        self.board[SQ_NUM // 2][SQ_NUM // 2 - 1] = Stone.BLACK
        self.board[SQ_NUM // 2][SQ_NUM // 2] = Stone.WHITE
        self.state = State.PLAY
        self.turn = Stone.BLACK

    def is_pass(self):
        for y in range(SQ_NUM):
            for x in range(SQ_NUM):
                if self.is_put(y, x):
                    return False
        return True

    def is_put(self, y, x):
        """
        石を置ける場合は石をひっくり返すことができる方向を返し、
        置けない場合は空のリストを返す
        """
        directions = []
        if self.board[y][x] != Stone.EMPTY:
            return directions

        enemy = self.get_enemy()

        dyx = [(-1, -1), (-1, 0), (-1, 1),
               (0, -1), (0, 1),
               (1, -1), (1, 0), (1, 1)]
        for dy, dx in dyx:
            ny, nx = y + dy, x + dx
            if ny < 0 or ny >= SQ_NUM or nx < 0 or nx >= SQ_NUM:
                continue
            if self.board[ny][nx] == enemy:
                ny, nx = ny + dy, nx + dx
                while 0 <= ny < SQ_NUM and 0 <= nx < SQ_NUM:
                    if self.board[ny][nx] == self.turn:
                        directions.append((dy, dx))
                        break
                    elif self.board[ny][nx] == Stone.EMPTY:
                        break
                    ny, nx = ny + dy, nx + dx
        return directions

    def turn_action(self, y, x):
        directions = self.is_put(y, x)
        if directions:
            self.board[y][x] = self.turn
            self.flip_board(y, x, directions)
            self.check_gameover()
            self.change_turn()
