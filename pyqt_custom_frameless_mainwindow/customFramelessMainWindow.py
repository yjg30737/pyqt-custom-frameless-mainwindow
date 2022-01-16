from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt, QPoint


class CustomFramelessMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__margin = 5
        self.__cursor = QCursor()
        self.__rect = 0

        self.__top = False
        self.__bottom = False
        self.__left = False
        self.__right = False

        self.__min_width = 30
        self.__min_height = 30

        self.__hoveredOnEdge = False
        self.__resizeEnabled = False

        self.__offset = 0
        self.__moving = False

        self.__initUi()

    def __initUi(self):
        self.setMouseTracking(True)
        self.setWindowFlags(Qt.FramelessWindowHint)

    def __setSizeCursor(self, p):
        rect = self.rect()
        rect.setX(self.rect().x()+self.__margin)
        rect.setY(self.rect().y()+self.__margin)
        rect.setWidth(self.rect().width()-self.__margin*2)
        rect.setHeight(self.rect().height()-self.__margin*2)

        if rect.contains(p):
            # reshape cursor for moving
            self.unsetCursor()
            self.__cursor = self.cursor()

            self.__top = False
            self.__bottom = False
            self.__right = False
            self.__left = False
        else:
            # reshape cursor for resizing
            x = p.x()
            y = p.y()

            x1 = self.rect().x()
            y1 = self.rect().y()
            x2 = self.rect().width()
            y2 = self.rect().height()

            self.__left = abs(x-x1) <= self.__margin
            self.__top = abs(y-y1) <= self.__margin
            self.__right = abs(x-(x2+x1)) <= self.__margin
            self.__bottom = abs(y-(y2+y1)) <= self.__margin

            if self.__top and self.__left:
                self.__cursor.setShape(Qt.SizeFDiagCursor)
            elif self.__top and self.__right:
                self.__cursor.setShape(Qt.SizeBDiagCursor)
            elif self.__bottom and self.__left:
                self.__cursor.setShape(Qt.SizeBDiagCursor)
            elif self.__bottom and self.__right:
                self.__cursor.setShape(Qt.SizeFDiagCursor)
            elif self.__left:
                self.__cursor.setShape(Qt.SizeHorCursor)
            elif self.__top:
                self.__cursor.setShape(Qt.SizeVerCursor)
            elif self.__right:
                self.__cursor.setShape(Qt.SizeHorCursor)
            elif self.__bottom:
                self.__cursor.setShape(Qt.SizeVerCursor)
            self.setCursor(self.__cursor)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.__hoveredOnEdge:
                # resizing start
                self.__resizeEnabled = True
            else:
                # moving start
                p = e.pos()
                self.__offset = p
                self.__moving = True
        return super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        if self.__resizeEnabled:
            # resizing
            self.__rect = self.rect()
            p = e.pos()
            x = p.x()
            y = p.y()
            if self.__cursor.shape() == Qt.SizeHorCursor:
                if self.__left:
                    self.__rect.setLeft(x)
                elif self.__right:
                    self.__rect.setRight(x)
            elif self.__cursor.shape() == Qt.SizeVerCursor:
                if self.__top:
                    self.__rect.setTop(y)
                elif self.__bottom:
                    self.__rect.setBottom(y)
            elif self.__cursor.shape() == Qt.SizeBDiagCursor:
                if self.__top and self.__right:
                    self.__rect.setTopRight(QPoint(x, y))
                elif self.__bottom and self.__left:
                    self.__rect.setBottomLeft(QPoint(x, y))
            elif self.__cursor.shape() == Qt.SizeFDiagCursor:
                if self.__top and self.__left:
                    self.__rect.setTopLeft(QPoint(x, y))
                elif self.__bottom and self.__right:
                    self.__rect.setBottomRight(QPoint(x, y))
        else:
            p = e.pos()
            # reshaping cursor
            self.__setSizeCursor(p)
            self.__hoveredOnEdge = not self.__isCursorHoveredOnInnerWidget(p)
            # if cursor shape indicates to resize
            if self.__hoveredOnEdge:
                pass
            # moving
            elif self.__moving:
                self.move(e.globalPos() - self.__offset)
        return super().mouseMoveEvent(e)

    def __isCursorHoveredOnInnerWidget(self, p):
        inner_rect = self.rect().adjusted(self.__margin, self.__margin, -self.__margin, -self.__margin)
        return inner_rect.contains(p)

    def mouseReleaseEvent(self, e):
        if self.__hoveredOnEdge and self.__resizeEnabled:
            # resizing end
            if self.__rect:
                global_top_left_p = self.mapToParent(self.__rect.topLeft())
                self.__rect.moveTopLeft(global_top_left_p)
                self.setGeometry(self.__rect)
                self.updateGeometry()
                self.__hoveredOnEdge = False
                self.__resizeEnabled = False
        else:
            # moving end
            self.__moving = False
        return super().mouseReleaseEvent(e)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    example = CustomFramelessMainWindow()
    example.show()
    app.exec_()