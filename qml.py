
# This Python file uses the following encoding: utf-8
import sys
import time
import os
import subprocess
import threading 

from inputs import get_gamepad


import paho.mqtt.client as mqtt

from urllib.request import urlopen
from PyQt5.QtCore import QObject, QUrl, Qt, pyqtProperty, pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType, QQmlEngine, QQmlComponent
from PyQt5 import QtCore, QtGui
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import QQmlContext


import platform


# if__name__ == "__main__":
#     pass
import sys
# Класс QUrl предоставляет удобный интерфейс для работы с Urls
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget
# Класс QQuickView предоставляет возможность отображать QML файлы.
from PyQt5.QtQuick import QQuickView


redirectory = "/home/pi/"


class QMLManipulate():
    def __init__(self):
        self.subject = self.findQmlByObjectCode('subject')


    def findQmlByObjectCode(self,objectCode):
        
        self.rootObjects()[0].findChild(QtCore.QObject, objectCode)

global status;
status = "turnedoff";
def on_connect(client, userdata, flags, rc):#
    print("Connected with result code "+str(rc))
    client.subscribe("toDevice/mainDisplay")
    client.subscribe("toDevice/ALL")
    client.publish("toServer/mainDisplay", payload='hello', qos=0, retain=False)
    client.publish("toServer/mainDisplay", payload=status, qos=0, retain=False)



def publish(message,device="toServer/mainDisplay"):
    client.publish(device, message)


def on_message(msg):
    newStatus = msg.payload.decode()
    global status#globali poxaren urish ban mtacel
    if newStatus == "status":
        print('status')
        publish(status)
    if(newStatus=="turnedoff"):
        status="turnedoff"
    if(newStatus=="standby"):
        status="standby"
        goStandby()
    if(newStatus=="startZenqiActivation1"):
        print('startZenqiActivation1')
        killVideo()
        launch.step1()
        
    if(newStatus=="startWelcomeVideo"):
        print('startWelcomeVideo')    
        # launch.startVideo1();
        startWelcomeVideo()
        launch.hide()
    if(newStatus=="killVideo"):
        killVideo()
        launch.hide()
    if(newStatus=="startEmulation"):
        launch.hide()
        startEmulation()

name = "mainDisplay"



omxp = None

def goStandby():
    #here will be player
    status = "standby"
    

def goTurnedOff():
    #here is video, that onnection problems
    status = ""

def startWelcomeVideo():
    movie_path = "./1.mp4"
    global omxp
    if(platform.system()=="Linux"):
        
        omxp = subprocess.Popen(['omxplayer',movie_path])
      #  print(type(omxp))
    else:
        omxp = subprocess.run(['open', movie_path], check=True)


def killVideo():
    #global omxp
    #if(omxp and platform.system()=="Linux"):
     #   omxp.kill()
    os.system('killall omxplayer.bin')
    os.system('killall emulationstation')
    os.system('killall emulationstatio')
    os.system('killall retroarch')
    
    # status = ""

def startEmulation():
    os.system('killall omxplayer.bin')
    os.system('killall emulationstation')
    os.system('killall retroarch')
    #subprocess.call("emulationstation", shell=True)
    #p = subprocess.Popen(['/opt/retropie/supplementary/runcommand/runcommand.sh', '0', '_SYS_', 'snes', '/home/pi/RetroPie/roms/snes/Space Megaforce (USA).sfc'])

    #p = subprocess.call(['/opt/retropie/emulators/retroarch/bin/retroarch -L /opt/retropie/libretrocores/lr-snes9x2010/snes9x2010_libretro.so --config /opt/retropie/configs/snes/retroarch.cfg "/home/pi/RetroPie/roms/snes/Space Megaforce (USA).sfc" --appendconfig /dev/shm/retroarch.cfg'])
    p=subprocess.call('/opt/retropie/emulators/retroarch/bin/retroarch -L /opt/retropie/libretrocores/lr-snes9x2010/snes9x2010_libretro.so --config /opt/retropie/configs/snes/retroarch.cfg "/home/pi/RetroPie/roms/snes/Space Megaforce (USA).sfc" --appendconfig /dev/shm/retroarch.cfg',shell=True)
    #askhatuma

def startFirstVideo():
    #here
    status = ""
    
def startStep2Video():
    status = ""

def startStep3Video():
    status = ""
def startStep4Video():
    status = ""

def startStep4FailedVideo():
    status = ""

class Launch(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.view = QQmlApplicationEngine()
        
        self.step = 1
        
    client_message = QtCore.pyqtSignal(object)
    textEdit = pyqtSignal(str,int, arguments=['text','step'])

    buttonPressed = pyqtSignal(bool, arguments=['pressed'])
    
    # слот
    @pyqtSlot(str)
    def textEdited(self, text):#stex piti stugvi iravichak@
      self.textEdit.emit(text, self.step)
      if(self.step == 1 and len(text)==3):
          
          QtCore.QTimer.singleShot(500, self.step2)


      elif(self.step==2 and len(text)==3):
          QtCore.QTimer.singleShot(500, self.step3)
      elif(self.step==3):
        text = ''
        
      #.....

    @pyqtSlot()
    def buttonPress(self):
        
        print("we are here baby")
        events = get_gamepad()
        for event in events:
            if(event.ev_type=='Key' and event.code=='BTN_THUMB'):
                self.buttonPressed.emit(event.state)
                    



    
        

    def initQML(self):
        
        self.view.rootContext().setContextProperty("launch", self)
        self.view.load(QUrl('qml.qml'))

        self.root = self.view.rootObjects()[0]
        self.root.setProperty('visible',False)
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

    def hideBlock(self,block):
       block.setProperty('stateVisible',0)
    def changeStep(self,nstep,text=''):
        self.step = nstep
        self.root.setProperty('step',nstep)
        self.textInput.setProperty('text', text)

    def step1(self):
        self.root.setProperty('visible',True)
        self.changeStep(1)
        self.textInput.forceActiveFocus()


        self.showBlock(self.weaponCodeBlock)
        self.hideBlock(self.coordinatesBlock)
        self.hideBlock(self.fireBlock)

        self.subject.setProperty('text', "Հավաքեք զենքի կոդը")

    def step2(self):
        self.changeStep(2)

        self.textInput.forceActiveFocus()

        self.showBlock(self.weaponCodeBlock)
        self.showBlock(self.coordinatesBlock)
        self.hideBlock(self.fireBlock)

        self.subject.setProperty('text', "Մուտքագրեք կոորդինատները")


    def step3(self):
        self.changeStep(3)



        self.showBlock(self.weaponCodeBlock)
        self.showBlock(self.coordinatesBlock)
        self.showBlock(self.fireBlock)
        self.subject.setProperty('text', "Սեղմեք կրակելու կոճակը")


        #openjar()
    def hide(self):
        self.root.setProperty('visible',False)



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



if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    launch = Launch()
    launch.initQML()
    client = mqtt.Client(name)
    client.connect("192.168.2.5",1883)
    #client.connect("192.168.2.2",1883)
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.on_message = lambda c, d, msg: launch.client_message.emit(msg)# ays masi shnorhiv a ashkhatel u pyqtsygnali. kareli a pordzel hanel classic durs, kam el hakarak@ mtcnel mej@
    launch.client_message.connect(on_message)
        
    client.loop_start()       
    

     
    
    #downloader = Downloader('https://cdimage.debian.org/debian-cd/current/armhf/iso-cd/debian-10.1.0-armhf-xfce-CD-1.iso')
    


    


    




    # Объект QQuickView, в который грузится UI для отображения

    #view = QtDeclarative.QDeclarativeView()
   # view.rootContext().setContextProperty("downloader", downloader)
  
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



