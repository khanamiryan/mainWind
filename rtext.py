import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import *
from random import randrange

class MyClass(QObject):

    randomText = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MyClass, self).__init__(parent)

    def random_text(self):
        x = str(randrange(1, 10))
        self.randomText.emit(x)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_obj = MyClass()

    timer = QTimer()
    timer.start(2000)

    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    ctx.setContextProperty("my_obj", my_obj)
    engine.load('rtext.qml')
    root = engine.rootObjects()[0]
    timer.timeout.connect(my_obj.random_text)
    my_obj.randomText.connect(root.title)
    sys.exit(app.exec_())