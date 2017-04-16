import copy
import enum
import cpu


SQ_NUM = 8  # COL,ROWの数
State = enum.Enum('State', 'START PLAY GAMEOVER')
Stone = enum.Enum('Stone', 'EMPTY BLACK WHITE')


def get_enemy(color):
    enemy = None
    if color == Stone.BLACK:
        enemy = Stone.WHITE
    else:
        enemy = Stone.BLACK
    return enemy


class UndoInfo(object):

    def __init__(self, y, x, points):
        self.y, self.x = y, x
        self.points = points

    def get_board(self, board):
        board[self.y][self.x] = Stone.EMPTY
        for point in self.points:
            y, x = point
            if board[y][x] == Stone.BLACK:
                board[y][x] = Stone.WHITE
            else:
                board[y][x] = Stone.BLACK
        return board


class ReversiBoard(object):

    def __init__(self):
        self.board = []
        self.init_board()

    def init_board(self):
        self.board = [[Stone.EMPTY for x in range(SQ_NUM)] for y in range(SQ_NUM)]
        self.board[SQ_NUM // 2 - 1][SQ_NUM // 2 - 1] = Stone.WHITE
        self.board[SQ_NUM // 2 - 1][SQ_NUM // 2] = Stone.BLACK
        self.board[SQ_NUM // 2][SQ_NUM // 2 - 1] = Stone.BLACK
        self.board[SQ_NUM // 2][SQ_NUM // 2] = Stone.WHITE

    def copy(self):
        copy_board = copy.deepcopy(self.board)
        return copy_board

    def flip_board(self, y, x, directions, color):
        points = self.get_flip_points(y, x, directions, color)
        for point in points:
            y, x = point
            self.board[y][x] = color
        return points

    def get_flip_points(self, y, x, directions, color):
        points = []
        for direction in directions:
            dy, dx = direction
            ny, nx = y + dy, x + dx
            while True:
                if self.board[ny][nx] == color:
                    break
                points.append((ny, nx))
                ny, nx = ny + dy, nx + dx
        return points

    def get_putable_points(self, color):
        points = []
        for y in range(SQ_NUM):
            for x in range(SQ_NUM):
                if self.is_put(y, x, color):
                    points.append((y, x))
        return points

    def is_pass(self, color):
        for y in range(SQ_NUM):
            for x in range(SQ_NUM):
                if self.is_put(y, x, color):
                    return False
        return True

    def is_put(self, y, x, color):
        """
        石を置ける場合は石をひっくり返すことができる方向を返し、
        置けない場合は空のリストを返す
        """
        directions = []
        if self.board[y][x] != Stone.EMPTY:
            return directions

        enemy = get_enemy(color)

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
                    if self.board[ny][nx] == color:
                        directions.append((dy, dx))
                        break
                    elif self.board[ny][nx] == Stone.EMPTY:
                        break
                    ny, nx = ny + dy, nx + dx
        return directions


class Reversi(object):

    def __init__(self):
        self.board = ReversiBoard()
        self.undo = []
        self.state = State.START
        self.turn = Stone.BLACK
        self.cpu_player = Stone.WHITE
        self.cpu = cpu.Cpu()
        self.init_game()

    def init_game(self):
        self.undo = []
        self.state = State.START
        self.turn = Stone.BLACK
        self.board.init_board()
        self.cpu_player = Stone.WHITE
        self.cpu.init_cpu(self.cpu_player)

    def change_turn(self):
        self.turn = get_enemy(self.turn)
        if self.board.is_pass(self.turn) and self.state == State.PLAY:
            self.turn = get_enemy(self.turn)

    def check_gameover(self):
        if (len(self.board.get_putable_points(Stone.BLACK)) == 0 and
                len(self.board.get_putable_points(Stone.WHITE)) == 0):
            self.state = State.GAMEOVER

    def get_score(self, color):
        count = 0
        for y in range(SQ_NUM):
            for x in range(SQ_NUM):
                if self.board.board[y][x] == color:
                    count += 1
        return count

    def turn_action(self, y, x):
        directions = self.board.is_put(y, x, self.turn)
        if directions:
            self.board.board[y][x] = self.turn
            points = self.board.flip_board(y, x, directions, self.turn)
            self.undo.append(UndoInfo(y, x, points))
            self.check_gameover()
            if self.state == State.PLAY:
                self.change_turn()

    def undo_board(self):
        if len(self.undo) == 0:
            return
        info = self.undo.pop()
        self.board = info.get_board(self.board)
