import random
import reversiCore


MAX_VALUE = 9999
MIN_VALUE = -9999
DEPTH = 4


class Cpu(object):

    def __init__(self):
        self.color = None
        self.board = reversiCore.ReversiBoard()

    def init_cpu(self, color):
        self.color = color

    # alphabeta
    def next_move(self, board, turn, depth=DEPTH, alpha=MIN_VALUE, beta=MAX_VALUE):
        if depth == 0:
            return self.value_board(board, turn)

        best_y, best_x = 0, 0
        alpha = -9999
        beta = 9999

        undo_board = None
        points = board.get_putable_points(turn)
        if points:
            for point in points:
                y, x = point
                directions = board.is_put(y, x, turn)
                flip_points = board.flip_board(y, x, directions, turn)
                undo_board = reversiCore.UndoInfo(y, x, flip_points)
                temp = self.next_move(board, reversiCore.get_enemy(turn), depth - 1,
                                      alpha, beta)
                board.board = undo_board.get_board(board.board)
                if turn == self.color:
                    if temp >= alpha:
                        alpha = temp
                        best_y = y
                        best_x = x
                    if alpha > beta:
                        return alpha
                else:
                    if temp <= beta:
                        beta = temp
                        best_y = y
                        best_x = x
                    if alpha > beta:
                        return beta
        else:
            temp = self.next_move(board, reversiCore.get_enemy(turn), depth - 1,
                                  alpha, beta)
            return temp

        if depth == DEPTH:
            return best_y, best_x
        elif turn == self.color:
            return alpha
        elif turn != self.color:
            return beta

    def value_board(self, board, turn):
        enemy = reversiCore.get_enemy(turn)
        value = 0
        eval_value = [[100, -40, 20, 5, 5, 20, -40, 100],
                      [-40, -80, -1, -1, -1, -1, -80, -40],
                      [20, -1, 5, 1, 1, 5, -1, 20],
                      [5, -1, 1, 0, 0, 1, -1, 5],
                      [5, -1, 1, 0, 0, 1, -1, 5],
                      [20, -1, 5, 1, 1, 5, -1, 20],
                      [-40, -80, -1, -1, -1, -1, -80, -40],
                      [100, -40, 20, 5, 5, 20, -40, 100]]
        for y in range(reversiCore.SQ_NUM):
            for x in range(reversiCore.SQ_NUM):
                if board.board[y][x] == turn:
                    value += eval_value[y][x]
                elif board.board[y][x] == enemy:
                    value -= eval_value[y][x]
        return value


class Level0(object):

    def __init__(self):
        self.color = None

    def init_cpu(self, color):
        self.color = color

    def next_move(self, board):
        putable_points = board.get_putable_points(self.color)
        y, x = putable_points[random.randint(0, len(putable_points) - 1)]
        return (y, x)
