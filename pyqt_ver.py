from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QFont, QFontMetrics
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsScene, QGraphicsView,
                             QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget)
import sys
import reversiCore


SQ_SIZE = 50  # 1マスの大きさ
BOARD_SIZE = reversiCore.SQ_NUM * SQ_SIZE  # 盤面の大きさ


class Game(QGraphicsItem):

    def __init__(self):
        super(Game, self).__init__()
        self.reversi = reversiCore.Reversi()
        # ラベル初期化
        self.turn_label = QLabel()
        self.stone_label = QLabel()
        self.update_turn_label()
        self.update_stone_label()

    def boundingRect(self):
        return QRectF(0, 0, BOARD_SIZE, BOARD_SIZE)

    def paint(self, painter, option, widget=None):
        # 盤面描画
        painter.setPen(Qt.black)
        for y in range(reversiCore.SQ_NUM):
            for x in range(reversiCore.SQ_NUM):
                painter.setBrush(QColor(40, 145, 30))
                painter.drawRect(x * SQ_SIZE, y * SQ_SIZE,
                                 SQ_SIZE, SQ_SIZE)
                if self.reversi.board[y][x] == reversiCore.Stone.BLACK:
                    painter.setBrush(QColor(0, 0, 0))
                    painter.drawEllipse(x * SQ_SIZE, y * SQ_SIZE,
                                        SQ_SIZE, SQ_SIZE)
                elif self.reversi.board[y][x] == reversiCore.Stone.WHITE:
                    painter.setBrush(QColor(255, 255, 255))
                    painter.drawEllipse(x * SQ_SIZE, y * SQ_SIZE,
                                        SQ_SIZE, SQ_SIZE)
        # 勝敗表示
        font = QFont()
        font.setPixelSize(60)
        fm = QFontMetrics(font)
        height = fm.height()
        painter.setFont(font)
        painter.setPen(Qt.red)
        s = ''
        if self.reversi.state == reversiCore.State.GAMEOVER:
            black, white = self.reversi.get_black_score(), self.reversi.get_white_score()
            if black > white:
                s = 'BLACK WIN!!'
            elif black < white:
                s = 'WHITE WIN!!'
            elif black == white:
                s = 'DRAW!!'
            width = fm.width(s)
            painter.drawText((BOARD_SIZE - width) / 2, (BOARD_SIZE - height) / 2, s)

    def update_label(self):
        self.update_turn_label()
        self.update_stone_label()

    def update_turn_label(self):
        if self.reversi.turn == reversiCore.Stone.BLACK:
            self.turn_label.setText('Current Player: Black')
        else:
            self.turn_label.setText('Current Player: White')

    def update_stone_label(self):
        self.stone_label.setText('B:{}  W:{}'.format(self.reversi.get_black_score(),
                                                     self.reversi.get_white_score()))


class GameView(QGraphicsView):

    def __init__(self):
        super(GameView, self).__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.game = Game()
        self.scene.addItem(self.game)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def mousePressEvent(self, event):
        pos = event.pos()
        x, y = int(pos.x() // SQ_SIZE), int(pos.y() // SQ_SIZE)
        self.game.reversi.turn_action(y, x)
        self.game.update()
        self.game.update_label()
        # CPU
        if (self.game.reversi.state == reversiCore.State.PLAY and
                self.game.reversi.turn == self.game.reversi.cpu_player):
            self.game.reversi.cpu()
            self.game.update()
            self.game.update_label()


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.game_view = GameView()

        self.property_layout = QHBoxLayout()
        self.property_layout.addWidget(self.game_view.game.turn_label)
        self.property_layout.addWidget(self.game_view.game.stone_label)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.game_view)
        self.main_layout.addLayout(self.property_layout)

        self.setLayout(self.main_layout)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()


if __name__ == '__main__':
    main()
