from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QWidget
class Color(QWidget):
    def __init__(self,color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.Window,QColor(color))
        self.setPalette(pal)