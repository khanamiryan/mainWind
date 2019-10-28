# This Python file uses the following encoding: utf-8
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys  # sys нужен для передачи argv в QApplication

import os
import testui as design  # Это наш конвертированный файл дизайна



class mainWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        #self.btnBrowse.clicked.connect(self.browse_folder)

        self.progressBar.setValue(0)
        self.infoTextProgress.setText('')
        self.step = 1
        self.step1()
        self.lineEdit.textChanged.connect(self.validate_text)

        #self.progressBar.setStyleSheet(
         #   " QProgressBar { border: 2px solid grey; border-radius: 0px; text-align: center; } QProgressBar::chunk {background-color: #3add36; width: 1px;}")


        #self.lineEdit.setInputMask('999')

    def validate_text(self):
        #self.lcdNumber.display(self.lineEdit.text())
        #print(self.lineEdit.text())
        if self.step ==1 and self.lineEdit.text() == "ASH":
            self.step = 2
            self.step2()
        if self.step == 2 and self.lineEdit.text() == "342":
            self.step = 3
            self.step3()




    def step1(self):
        self.label.setText('Հավաքեք զենքի կոդը')

    def step2(self):
        self.lineEdit.setText('')
        self.lineEdit.setCursorPosition(0)
        self.progressBar.setValue(20)
        self.label.setText('Հավաքեք կոորդինատները')
        text = self.infoTextProgress.text() + "Զենքի կոդը: ASH\n"
        self.infoTextProgress.setText(text)

    def step3(self):
        self.lineEdit.setText('')
        self.lineEdit.setCursorPosition(0)
        self.progressBar.setValue(50)
        self.label.setText('Սեղմեք կոճակը')
        text = self.infoTextProgress.text() + "Կոորդինատները: 342\n"
        self.infoTextProgress.setText(text)



    def progressbarAnimation(self,value):
        self.progressBar.setValue(0)
    def browse_folder(self):
        self.listWidget.clear()  # На случай, если в списке уже есть элементы
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к выбранной директории

        if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
            for file_name in os.listdir(directory):  # для каждого файла в директории
                self.listWidget.addItem(file_name)  # добавить файл в listWidget






def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    window = mainWindow()  # Создаём объект класса ExampleApp
    #window.show()  # Показываем окно

    screenGeometry = app.desktop().screenGeometry()

    x = (screenGeometry.width() - window.width()) / 2

    y = (screenGeometry.height() - window.height()) / 2
    window.move(x, y)
    window.show()
    #app.exec_()  # и запускаем приложение
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


