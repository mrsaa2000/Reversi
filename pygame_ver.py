import pygame
from pygame.locals import *
import reversiCore
import sys


SQ_SIZE = 50
BOARD_SIZE = reversiCore.SQ_NUM * SQ_SIZE
SCR_RECT = Rect(0, 0, reversiCore.SQ_NUM * SQ_SIZE, reversiCore.SQ_NUM * SQ_SIZE + 20)


class Game(object):

    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        self.reversi = reversiCore.Reversi()
        clock = pygame.time.Clock()
        while True:
            clock.tick(30)
            self.event_handler()
            self.draw(screen)
            pygame.display.update()

    def draw(self, screen):
        screen.fill((255, 255, 255))
        self.draw_board(screen)
        self.draw_text(screen)
        if self.reversi.state == reversiCore.State.GAMEOVER:
            self.draw_result(screen)

    def draw_board(self, screen):
        pygame.draw.rect(screen, (40, 145, 30), Rect(0, 0, BOARD_SIZE, BOARD_SIZE))
        for y in range(reversiCore.SQ_NUM):
            for x in range(reversiCore.SQ_NUM):
                pygame.draw.rect(screen, (0, 0, 0),
                                 Rect(x * SQ_SIZE, y * SQ_SIZE, SQ_SIZE, SQ_SIZE), 1)
                if self.reversi.board[y][x] == reversiCore.Stone.BLACK:
                    pygame.draw.ellipse(screen, (0, 0, 0),
                                        Rect(x * SQ_SIZE + 1, y * SQ_SIZE + 1,
                                             SQ_SIZE - 1, SQ_SIZE - 1))
                elif self.reversi.board[y][x] == reversiCore.Stone.WHITE:
                    pygame.draw.ellipse(screen, (255, 255, 255),
                                        Rect(x * SQ_SIZE + 1, y * SQ_SIZE + 1,
                                             SQ_SIZE - 1, SQ_SIZE - 1))

    def draw_text(self, screen):
        font = pygame.font.SysFont(None, 25)
        player = ''
        if self.reversi.turn == reversiCore.Stone.BLACK:
            player = 'Black'
        else:
            player = 'White'
        turn_text = 'CurrentPlayer: {}'.format(player)
        score_text = 'B:{} W:{}'.format(self.reversi.get_black_score(),
                                        self.reversi.get_white_score())
        turn = font.render(turn_text, True, (0, 0, 0))
        score = font.render(score_text, True, (0, 0, 0))
        screen.blit(turn, (0, BOARD_SIZE))
        screen.blit(score, (BOARD_SIZE - font.size(score_text)[0], BOARD_SIZE))

    def draw_result(self, screen):
        font = pygame.font.SysFont(None, 100)
        s = ''
        black = self.reversi.get_black_score()
        white = self.reversi.get_white_score()
        if black > white:
            s = 'BLACK WIN!!'
        elif black < white:
            s = 'WHITE WIN!!'
        elif black == white:
            s = 'DROW!!'
        result = font.render(s, True, (255, 0, 0))
        screen.blit(result, ((BOARD_SIZE - font.size(s)[0]) / 2, 0))

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = int(event.pos[0] // SQ_SIZE), int(event.pos[1] // SQ_SIZE)
                self.reversi.turn_action(y, x)
                if (self.reversi.state == reversiCore.State.PLAY and
                        self.reversi.turn == self.reversi.cpu_player):
                    self.reversi.cpu()


if __name__ == '__main__':
    Game()