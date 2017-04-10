import os
import sys
import threading
import pygame
from pygame.locals import *
import reversiCore
from reversiCore import Stone, State, SQ_NUM


SQ_SIZE = 50
BOARD_SIZE = SQ_NUM * SQ_SIZE
SCR_RECT = Rect(0, 0, SQ_NUM * SQ_SIZE, SQ_NUM * SQ_SIZE + 20)
BLACK_IMG = pygame.image.load(os.path.join('img', 'black.png'))
WHITE_IMG = pygame.image.load(os.path.join('img', 'white.png'))


class FlipStone(pygame.sprite.Sprite):

    speed = 3

    def __init__(self, y, x, color):
        super(FlipStone, self).__init__(self.containers)
        self.before = WHITE_IMG
        self.after = BLACK_IMG
        if color == Stone.WHITE:
            self.before = BLACK_IMG
            self.after = WHITE_IMG
        self.image = self.before
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.is_before = True  # 返す前か
        self.rect = self.image.get_rect(topleft=(x * SQ_SIZE, y * SQ_SIZE))

    def update(self):
        if self.is_before:
            self.rect.move_ip(self.speed / 2, 0)
            if self.width == 1:
                self.image = pygame.transform.scale(self.after, (self.width, self.height))
                self.is_before = False
            else:
                self.width -= self.speed
                if self.width <= 1:
                    self.width = 1
                self.image = pygame.transform.scale(self.before, (self.width, self.height))
        else:
            self.rect.move_ip(-self.speed / 2, 0)
            if self.image.get_width() >= self.after.get_width():
                self.before, self.after = self.after, self.before
                self.image = self.before
                super(FlipStone, self).kill()
            else:
                self.width += self.speed
                self.image = pygame.transform.scale(self.after, (self.width, self.height))


class Game(object):

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCR_RECT.size)
        clock = pygame.time.Clock()
        self.reversi = reversiCore.Reversi()
        # sprite group
        self.all = pygame.sprite.RenderUpdates()
        FlipStone.containers = self.all
        self.flip_stones = [[None for x in range(SQ_NUM)] for y in range(SQ_NUM)]
        while True:
            clock.tick(60)
            self.event_handler()
            self.draw()
            pygame.display.update()

    def change_turn(self):
        self.reversi.turn = reversiCore.get_enemy(self.reversi.turn)
        # パス
        if self.reversi.board.is_pass(self.reversi.turn):
            self.reversi.turn = reversiCore.get_enemy(self.reversi.turn)
            # player側がパスされた場合
            if self.reversi.turn == self.reversi.cpu_player:
                cpu = threading.Thread(target=self.cpu_action, name='cpu')
                cpu.start()

    def cpu_action(self):
        pygame.time.wait(1000)
        self.reversi.cpu.board.board = self.reversi.board.copy()
        y, x = self.reversi.cpu.next_move(self.reversi.cpu.board, self.reversi.cpu_player)
        self.turn_action(y, x)

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.draw_board()
        self.draw_text()
        self.all.draw(self.screen)
        self.all.update()
        if self.reversi.state == State.GAMEOVER:
            self.draw_result()

    def draw_board(self):
        """盤面描画"""
        pygame.draw.rect(self.screen, (40, 145, 30), Rect(0, 0, BOARD_SIZE, BOARD_SIZE))
        for y in range(SQ_NUM):
            for x in range(SQ_NUM):
                pygame.draw.rect(self.screen, (0, 0, 0),
                                 Rect(x * SQ_SIZE, y * SQ_SIZE, SQ_SIZE, SQ_SIZE), 1)
                # アニメーション中は表示しない
                if not self.flip_stones[y][x] or not self.flip_stones[y][x].alive():
                    if self.reversi.board.board[y][x] == Stone.BLACK:
                        self.screen.blit(BLACK_IMG, (x * SQ_SIZE, y * SQ_SIZE))
                    elif self.reversi.board.board[y][x] == Stone.WHITE:
                        self.screen.blit(WHITE_IMG, (x * SQ_SIZE, y * SQ_SIZE))

    def draw_text(self):
        """現在のプレイヤーと石の数の表示"""
        font = pygame.font.SysFont(None, 25)
        player = ''
        if self.reversi.turn == Stone.BLACK:
            player = 'Black'
        else:
            player = 'White'
        turn = font.render('CurrentPlayer: {}'.format(player), True, (0, 0, 0))
        score = font.render('B:{} W:{}'.format(self.reversi.get_score(Stone.BLACK),
                                               self.reversi.get_score(Stone.WHITE)),
                            True, (0, 0, 0))
        self.screen.blit(turn, (0, BOARD_SIZE))
        self.screen.blit(score, (BOARD_SIZE - score.get_width(), BOARD_SIZE))

    def draw_result(self):
        """勝敗表示"""
        result_font = pygame.font.SysFont(None, 80)
        replay_font = pygame.font.SysFont(None, 25)
        s = ''
        black = self.reversi.get_score(Stone.BLACK)
        white = self.reversi.get_score(Stone.WHITE)
        if black > white:
            s = 'BLACK WIN!!'
        elif black < white:
            s = 'WHITE WIN!!'
        elif black == white:
            s = 'DROW!!'
        result = result_font.render(s, True, (255, 0, 0))
        replay = replay_font.render('SpaceKey: Replay', True, (255, 0, 0))
        self.screen.blit(result, (((BOARD_SIZE - result.get_width()) / 2,
                                   (BOARD_SIZE - result.get_height()) / 2)))
        self.screen.blit(replay, (((BOARD_SIZE - replay.get_width()) / 2,
                                   ((BOARD_SIZE - result.get_height()) / 2 + 100))))

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = int(event.pos[0] // SQ_SIZE), int(event.pos[1] // SQ_SIZE)
                if 0 <= x < SQ_NUM and 0 <= y < SQ_NUM:
                    if self.reversi.state == State.START:
                        self.reversi.state = State.PLAY
                    self.turn_action(y, x)
                    if (self.reversi.state == State.PLAY and
                            self.reversi.turn == self.reversi.cpu_player):
                        cpu = threading.Thread(target=self.cpu_action, name='cpu')
                        cpu.start()
            if event.type == KEYDOWN and event.key == K_SPACE:
                if self.reversi.state == State.GAMEOVER:
                    self.reversi.init_game()
            if event.type == KEYDOWN and event.key == K_RETURN:
                if self.reversi.state == State.START:
                    self.select_after_attack()
            if event.type == KEYDOWN and event.key == K_u:
                if self.reversi.state == State.PLAY:
                    self.undo_board()

    def select_after_attack(self):
        """player側が後攻(白)を選んだ場合"""
        self.reversi.cpu_player = Stone.BLACK
        self.reversi.cpu.init_cpu(self.reversi.cpu_player)
        self.reversi.state = State.PLAY
        cpu = threading.Thread(target=self.cpu_action, name='cpu')
        cpu.start()

    def turn_action(self, y, x):
        directions = self.reversi.board.is_put(y, x, self.reversi.turn)
        if directions:
            self.reversi.board.board[y][x] = self.reversi.turn
            flip_points = self.reversi.board.get_flip_points(y, x, directions,
                                                             self.reversi.turn)
            self.reversi.undo.append(reversiCore.UndoInfo(y, x, flip_points))
            for flip_point in flip_points:
                f_y, f_x = flip_point
                self.flip_stones[f_y][f_x] = FlipStone(f_y, f_x, self.reversi.turn)
                self.reversi.board.board[f_y][f_x] = self.reversi.turn
            self.reversi.check_gameover()
            if self.reversi.state == State.PLAY:
                self.change_turn()

    def undo_board(self):
        if len(self.reversi.undo) <= 1:
            return
        self.reversi.undo_board()
        self.reversi.undo_board()


if __name__ == '__main__':
    Game()
