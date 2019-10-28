
# This Python file uses the following encoding: utf-8
import sys
import time
import os
import subprocess
import threading
from urllib.request import urlopen
from PyQt5.QtCore import QObject, QUrl, Qt, pyqtProperty, pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType, QQmlEngine, QQmlComponent
from PyQt5 import QtCore, QtGui
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import QQmlContext




# if__name__ == "__main__":
#     pass
import sys
# Класс QUrl предоставляет удобный интерфейс для работы с Urls
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget
# Класс QQuickView предоставляет возможность отображать QML файлы.
from PyQt5.QtQuick import QQuickView

class QMLManipulate():
    def __init__(self):
        self.subject = self.findQmlByObjectCode('subject')
    def findQmlByObjectCode(self,objectCode):
        print(self.view.rootObjects())
        self.view.rootObjects()[0].findChild(QtCore.QObject, objectCode)


class Launch(QtCore.QObject):
    def __init__(self, view):
        self.view = view
        QtCore.QObject.__init__(self)
        self.step = 1

    textEdit = pyqtSignal(str,int, arguments=['text','step'])



    # слот для суммирования двух чисел
    @pyqtSlot(str)
    def textEdited(self, text):
      self.textEdit.emit(text, self.step)
      if(self.step == 1 and len(text)==3):
            self.step2()

      elif(self.step==2 and len(text)==3):
            self.step3()
      elif(self.step==3):
          text = ''
      #.....



    def initQML(self):
        self.root = self.view.rootObjects()[0]
        self.subject = self.findQmlByObjectCode('subject')
        self.textInput = self.findQmlByObjectCode('textInput')
        self.weaponCodeBlock = self.findQmlByObjectCode('weaponCodeBlock')
        #self.weaponCodeText = self.findQmlByObjectCode('weaponCodeText')
        self.coordinatesBlock = self.findQmlByObjectCode('coordinatesBlock')
        #self.coordinatesText = self.findQmlByObjectCode('coordinatesText')
        self.fireBlock = self.findQmlByObjectCode('fireBlock')

    def findQmlByObjectCode(self,objectCode):

        return self.view.rootObjects()[0].findChild(QtCore.QObject, objectCode)

    def showBlock(self,block):
       block.setProperty('stateVisible',1)

    def hideBlock(self,blockID):
       block.setProperty('stateVisible',0)
    def changeStep(self,nstep):
        self.step = nstep
        self.root.setProperty('step',nstep)
        self.textInput.setProperty('text','')

    def step1(self):

        self.changeStep(1)
        self.textInput.forceActiveFocus()


        self.showBlock(self.weaponCodeBlock)
        self.subject.setProperty('text', "Հավաքեք զենքի կոդը")

    def step2(self):
        self.changeStep(2)

        self.textInput.forceActiveFocus()

        self.showBlock(self.coordinatesBlock)
        self.subject.setProperty('text', "Մուտքագրեք կոորդինատները")


    def step3(self):
        self.changeStep(3)

        self.textInput.setProperty('focus',0)


        self.showBlock(self.fireBlock)
        self.subject.setProperty('text', "Սեղմեք կրակելու կոճակը")
        openjar()



def openjar():
    global bsnes
    print("Nintaco")
    bsnes = subprocess.Popen(['wine','wine /Users/Ashot/Desktop/snes9x-rr-1.60-win32-x64/snes9x-x64.exe -fullscreen /Users/Ashot/Desktop/Space\ Megaforce\ \(USA\).zip'],stdout=subprocess.PIPE)
    output = bsnes.communicate()[0]
    print(output)

def hideShow(r):

     stateVisible = r.property('stateVisible')
     #visible = r.property('visible')

     r.setProperty('stateVisible',not stateVisible)

     #r.setProperty('visible', not visible)

     t = threading.Timer(2.0, hideShow, [r])
     t.start();


class Downloader(QtCore.QObject):
    def __init__(self, url, filename=None):
        QtCore.QObject.__init__(self)
        self._url = url

        if filename is None:
            filename = os.path.basename(self._url)

        self._filename = filename
        self._progress = 0.
        self._running = False
        self._size = -1










    def _download(self):

        self.on_size.emit()
        self.progress = 10

        self.running = True





    @QtCore.pyqtSlot()
    def start_download(self):
        if not self.running:
            self.running = True

        thread = threading.Thread(target=self._download)
        thread.start()

    def _get_progress(self):
        return self._progress

    def _set_progress(self, progress):
        self._progress = progress
        self.on_progress.emit()

    def _get_running(self):
        return self._running

    def _set_running(self, running):
        self._running = running
        self.on_running.emit()

    def _get_filename(self):
        return self._filename

    def _get_size(self):
        return self._size

    on_progress = QtCore.pyqtSignal()
    on_running = QtCore.pyqtSignal()
    on_filename = QtCore.pyqtSignal()
    on_size = QtCore.pyqtSignal()


    progress = QtCore.pyqtProperty(float, _get_progress, _set_progress, notify=on_progress)
    running = QtCore.pyqtProperty(bool, _get_running, _set_running, notify=on_running)
    filename = QtCore.pyqtProperty(str, _get_filename, notify=on_filename)
    size = QtCore.pyqtProperty(int, '', _get_size, notify=on_size)




if __name__ == '__main__':


    app = QApplication(sys.argv)

    downloader = Downloader('https://cdimage.debian.org/debian-cd/current/armhf/iso-cd/debian-10.1.0-armhf-xfce-CD-1.iso')
    view = QQmlApplicationEngine()


    launch = Launch(view);

    # Объект QQuickView, в который грузится UI для отображения

    #view = QtDeclarative.QDeclarativeView()
    view.rootContext().setContextProperty("downloader", downloader)
    view.rootContext().setContextProperty("launch", launch)




    #view.setResizeMode(QQuickView.SizeRootObjectToView)
    view.load(QUrl('qml.qml'))

    launch.initQML()
    launch.step1()
    #view.setContextProperty()
    #view.showFullScreen()



    #r = view.rootObjects()[0].findChild(QtCore.QObject, "fireBlock")
    #t = threading.Timer(2.0, hideShow, [r])
    #t.start();




    #gauge=view.findChild(QObject,'image4')

   # gauge.setProperty('visible',"false")

    #view.show()

    app.exec_()
    sys.exit()



