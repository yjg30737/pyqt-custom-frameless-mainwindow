from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QPoint


class CustomFramelessMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__margin = 3
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

    def setSizeCursor(self, p):
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

            self.__hoveredOnEdge = False
        else:
            # reshape cursor for resizing
            x = p.x()
            y = p.y()

            x1 = self.rect().x()
            y1 = self.rect().y()
            x2 = self.rect().width()
            y2 = self.rect().height()

            # Top left
            if abs(x-x1) <= self.__margin and abs(y-y1) <= self.__margin:
                self.__cursor.setShape(Qt.SizeFDiagCursor)
                self.__top = True
                self.__left = True
                self.__bottom = False
                self.__right = False
                self.setCursor(self.__cursor)

            # Top right
            elif abs(x-(x2+x1)) <= self.__margin and abs(y-y1) <= self.__margin:
                self.__cursor.setShape(Qt.SizeBDiagCursor)
                self.__top = True
                self.__right = True
                self.__bottom = False
                self.__left = False
                self.setCursor(self.__cursor)

            # Bottom left
            elif abs(x-x1) <= self.__margin and abs(y-(y2+y1)) <= self.__margin:
                self.__cursor.setShape(Qt.SizeBDiagCursor)
                self.__bottom = True
                self.__left = True
                self.__top = False
                self.__right = False
                self.setCursor(self.__cursor)

            # Bottom right
            elif abs(x-(x2+x1)) <= self.__margin and abs(y-(y2+y1)) <= self.__margin:
                self.__cursor.setShape(Qt.SizeFDiagCursor)
                self.__bottom = True
                self.__right = True
                self.__top = False
                self.__left = False
                self.setCursor(self.__cursor)

            # Top
            elif abs(y-y1) <= self.__margin:
                self.__top = True
                self.__right = False
                self.__left = False
                self.__bottom = False
                self.__cursor.setShape(Qt.SizeVerCursor)
                self.setCursor(self.__cursor)

            # Bottom
            elif abs(y-(y2+y1)) <= self.__margin:
                self.__bottom = True
                self.__right = False
                self.__left = False
                self.__top = False
                self.__cursor.setShape(Qt.SizeVerCursor)
                self.setCursor(self.__cursor)

            # Left
            elif abs(x-x1) <= self.__margin:
                self.__left = True
                self.__right = False
                self.__top = False
                self.__bottom = False
                self.__cursor.setShape(Qt.SizeHorCursor)
                self.setCursor(self.__cursor)

            # Right
            elif abs(x-(x2+x1)) <= self.__margin:
                self.__right = True
                self.__left = False
                self.__top = False
                self.__bottom = False
                self.__cursor.setShape(Qt.SizeHorCursor)
                self.setCursor(self.__cursor)

    def mousePressEvent(self, e):
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
                if self.__left and self.__rect.right()-x > self.__min_width:
                    self.__rect.setLeft(x)
                elif self.__right and x > 30:
                    self.__rect.setRight(x)
            elif self.__cursor.shape() == Qt.SizeVerCursor:
                if self.__top and self.__rect.bottom()-y > self.__min_height:
                    self.__rect.setTop(y)
                elif self.__bottom and y > self.__min_height:
                    self.__rect.setBottom(y)
            elif self.__cursor.shape() == Qt.SizeBDiagCursor:
                if self.__top and self.__right and x > self.__min_width and self.__rect.bottom()-y > self.__min_height:
                    self.__rect.setTopRight(QPoint(x, y))
                elif self.__bottom and self.__left and self.__rect.right()-x > self.__min_width and y > self.__min_height:
                    self.__rect.setBottomLeft(QPoint(x, y))
            elif self.__cursor.shape() == Qt.SizeFDiagCursor:
                if self.__top and self.__left and self.__rect.right()-x > self.__min_width and self.__rect.bottom()-y > self.__min_height:
                    self.__rect.setTopLeft(QPoint(x, y))
                elif self.__bottom and self.__right and x > self.__min_width and y > self.__min_height:
                    self.__rect.setBottomRight(QPoint(x, y))
        else:
            p = e.pos()
            # reshaping cursor
            self.setSizeCursor(p)
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