import sys
import time
import os
import subprocess
import threading

import paho.mqtt.client as mqtt

from urllib.request import urlopen
from PyQt5.QtCore import QObject, QUrl, Qt, pyqtProperty, pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType, QQmlEngine, QQmlComponent
from PyQt5 import QtCore, QtGui
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import QQmlContext


if __name__ == '__main__':


    app = QApplication(sys.argv)

    
    view = QQmlApplicationEngine()


    
  
    

    app.exec_()
    sys.exit()
