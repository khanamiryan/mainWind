
# This Python file uses the following encoding: utf-8
import sys
import time
import os
import subprocess
import threading
import pyautogui

from inputs import get_gamepad


import paho.mqtt.client as mqtt

from urllib.request import urlopen
from PyQt5.QtCore import QObject, QUrl, Qt, pyqtProperty, pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType, QQmlEngine, QQmlComponent
from PyQt5 import QtCore, QtGui
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import QQmlContext


from omxplayer.player import OMXPlayer
from pathlib import Path


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
status = "standby";
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
        print(status)
        publish(status)
    if(newStatus=="turnedoff"):
        status="turnedoff"
        goTurnedOff()
    if(newStatus=="standby"):
        status="standby"
        goStandby()


        
    if(newStatus=="resetBlocks"):
        launch.resetBlocks()

    if(newStatus=="startWelcomeVideo"):
        startVideo("Welcome")        

    if(newStatus=="startFirstVideo"):
        startVideo("First")      

    if(newStatus=="startStep2Video"):
        startVideo("Step2")

    if(newStatus=="startStep3Video"):
        startVideo("Step3")
    if(newStatus=="startStep4Video"):
        startVideo("Step4")
    if(newStatus == "startFirstWeaponUseVideo"):#arajin angam zenqi havaqelna, vor traquma zenq@
        startVideo("FirstWeaponUse",False)
    if(newStatus == "startFirstWeaponUse"):#arajin angam zenqi havaqelna, vor traquma zenq@
        killVideo()
        launch.step3ForFail()
    if(newStatus=="startStep6Video"):##lazerov petqa licqavoren, asuma vor sxal en krakel, ruchnoy piti licqavoren anen, petqa mi qani angam asi es mek@
        startVideo("Step6")
    if(newStatus=="startStep7Video"):##video, voric heto arden piti havaqen kod@
        startVideo("Step7")

    if(newStatus=="startRealWeaponUse" or newStatus=="startZenqiActivation1"):
        launch.step1()
        time.sleep(2)
        killVideo()##petq en?

    if(newStatus=="startStep8Video"):##video, voric heto arden piti havaqen kod@
        startVideo("Step8")

    if(newStatus=="killVideo"):

        killVideo()
    if(newStatus=="startEmulation"):
        startEmulation()
    if(newStatus=="stopEmulation"):
        killEmulation()
        
    
    if(newStatus == "openEmulationMenu"):
       
        openEmulationMenu()

name = "mainDisplay"
displays = [2,7]# ekranneri kod@
players = {}


omxp = None
omxp2 = None
p = None
omxp_thread = None
emulationstate = False

def goStandby():
    #here will be player
    status = "standby"
    startSecondMonitor()
    startVideo("Standby")

def goTurnedOff():
    #here is video, that onnection problems
    status = "turnedoff"
    startVideo("Turnedoff")
    startSecondMonitor("turnedoff-secondary")



def player_position_thread(publish_text = "",minimal_position = 3):
    global omxp
    while True:
        # try omxp
        print("he is working")


        try:
            if(omxp.duration()-omxp.position()<minimal_position):#qani varkyana mnacel avartin
                publish(publish_text)
                print(publish_text)
                return "ok";
        except Exception as err: 
            print("****err*****", str(err))
            return "errroooo";


        time.sleep(1)
        

def startVideo(movie_path="1",loop=True,options=""):
    global omxp
    global omxp_thread
    
    if(platform.system()=="Linux"):

        VIDEO_PATH = Path("./videos/"+movie_path+".mp4")
        args='--aspect-mode fill --display 2 --no-osd --no-keys -b'
        if(loop==True):
            args+=' --loop'
        if(omxp is None):
            omxp = OMXPlayer(VIDEO_PATH,
                    dbus_name='org.mpris.MediaPlayer2.omxplayer1',args=args)
        else:
            omxp.load(VIDEO_PATH)
    
            killEmulation()##esim
            
        omxp_thread = threading.Thread(target=player_position_thread, args=(movie_path+"VideoEnded",))
        
        omxp_thread.start()    
        #omxp.mute() #heto hanel

        return omxp

    return False

def startSecondMonitor(movie_path="1",loop=True):
    global omxp2 
    
    if(platform.system()=="Linux"):
        VIDEO_PATH = Path("./videos/"+movie_path+".mp4")
        args='--aspect-mode fill --display 7 --no-osd --no-keys -b'
        if(loop==True):
            args+=' --loop'
        if(omxp2 is None):
            omxp2 = OMXPlayer(VIDEO_PATH,
                    dbus_name='org.mpris.MediaPlayer2.omxplayer2',args=args)
        else:
            omxp2.load(VIDEO_PATH)
        
        omxp2.mute()
        
        return omxp2
    
    return False



def openEmulationMenu():
    pyautogui.hotkey('tab', 'w',interval=0.1)
    
    


def killVideo():
    global omxp
    if(omxp is not None):
        omxp.quit()
    

def startEmulation():
    global p
    # os.system('killall omxplayer.bin')
    
    
     #subprocess.call("emulationstation", shell=True)
    #p = subprocess.Popen(['/opt/retropie/supplementary/runcommand/runcommand.sh', '0', '_SYS_', 'snes', '/home/pi/RetroPie/roms/snes/Space Megaforce (USA).sfc'])
    #p = subprocess.call(['/opt/retropie/emulators/retroarch/bin/retroarch -L /opt/retropie/libretrocores/lr-snes9x2010/snes9x2010_libretro.so --config /opt/retropie/configs/snes/retroarch.cfg "/home/pi/RetroPie/roms/snes/Space Megaforce (USA).sfc" --appendconfig /dev/shm/retroarch.cfg'])
    # pipe = subprocess.PIPE
    
    killEmulation()

    startVideo("emulationstart")#video sksum, vor sirun lini, chtarti

    p=subprocess.Popen('/opt/retropie/emulators/retroarch/bin/retroarch -L /opt/retropie/libretrocores/lr-snes9x2010/snes9x2010_libretro.so --config /opt/retropie/configs/snes/retroarch.cfg "/home/pi/RetroPie/roms/snes/Space Megaforce (USA).sfc" --appendconfig /dev/shm/retroarch.cfg',shell=True)
    emulationstate = True
    if(omxp is not None):
        time.sleep(2)
        omxp.quit()

    
    #askhatuma

def killEmulation():
    os.system('killall emulationstation 2>/dev/null')
    os.system('killall emulationstatio 2>/dev/null')
    os.system('killall retroarch 2>/dev/null')
    emulationstate = False


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
        

        
        gampead_t = threading.Thread(target=self.gamepad_thread, args=())
        gampead_t.daemon = True
        gampead_t.start()
            
            
        
    client_message = QtCore.pyqtSignal(object)
    textEdit = pyqtSignal(str,int, arguments=['text','step'])

    buttonPressed = pyqtSignal(bool, arguments=['pressed'])


    def gamepad_thread(self):
        while True:
            events = get_gamepad()
            for event in events:
                if(event.ev_type=='Key' and event.code=='BTN_THUMB'):
                    self.buttonPressed.emit(event.state)
                    
    
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

    @pyqtSlot(int,int, bool)
    def buttonPressFromQml(self,qmlStep,qmlSeconds,isWin):
        
        if(qmlStep==30 and isWin==False): #sexmel en knopkayin arajin krakelu jamanak
            publish("FirstWeaponFailed")

        if(qmlStep==3 and isWin==False):
            publish("RealWeaponUsedFailed")
            QtCore.QTimer.singleShot(5000, self.step1)
        elif(qmlStep==3 and isWin==True): 
            publish("RealWeaponUsedRight")
            print("winner")
            #QtCore.QTimer.singleShot(5000, self.step1)
           
        

       
                    
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

    def resetBlocks(self):
        self.hideBlock(self.weaponCodeBlock)
        self.hideBlock(self.coordinatesBlock)
        self.hideBlock(self.fireBlock)
        self.weaponCodeBlock.setProperty('text', "")
        self.coordinatesBlock.setProperty('text', "")
        self.fireBlock.setProperty('text', "")
        self.textInput.setProperty('text', "")
        self.subject.setProperty('sText', "")
        self.root.isWin = False



    def showBlock(self,block):
       block.setProperty('stateVisible',1)

    def hideBlock(self,block):
       block.setProperty('stateVisible',0)
    def changeStep(self,nstep,text=''):
        self.step = nstep
        self.root.setProperty('step',nstep)
        self.textInput.setProperty('text', text)

    def step1(self):
        self.resetBlocks()
        self.root.setProperty('visible',True)
        
        self.root.showFullScreen()
        
        self.changeStep(1)
        self.textInput.forceActiveFocus()
        self.showBlock(self.weaponCodeBlock)
        self.hideBlock(self.coordinatesBlock)
        self.hideBlock(self.fireBlock)

        self.subject.setProperty('sText', "Հավաքեք զենքի կոդը")

    def step2(self):
        self.root.setProperty('visible',True)
        self.root.showFullScreen()
        self.changeStep(2)

        self.textInput.forceActiveFocus()

        self.showBlock(self.weaponCodeBlock)
        self.showBlock(self.coordinatesBlock)
        self.hideBlock(self.fireBlock)

        self.subject.setProperty('sText', "Մուտքագրեք կոորդինատները")


    def step3(self):
        self.root.setProperty('visible',True)
        self.root.showFullScreen()
        self.changeStep(3)

        self.showBlock(self.weaponCodeBlock)
        self.showBlock(self.coordinatesBlock)
        self.showBlock(self.fireBlock)
        self.subject.setProperty('sText', "Սեղմեք կրակելու կոճակը")
        
    def step3ForFail(self):
        self.changeStep(30)
        #self.findQmlByObjectCode('countdown').
        
        
        
        self.hideBlock(self.weaponCodeBlock)
        self.hideBlock(self.coordinatesBlock)
        self.hideBlock(self.fireBlock)
        
        #self.showBlock(self.fireBlock)
        self.subject.setProperty('sText', "Սեղմեք կրակելու կոճակը")
        
        self.root.setProperty('visible',True)
        self.root.showFullScreen()


    def hide(self):
        self.root.setProperty('visible',False)



def hideShow(r):

     stateVisible = r.property('stateVisible')
     #visible = r.property('visible')

     r.setProperty('stateVisible',not stateVisible)

     #r.setProperty('visible', not visible)

     t = threading.Timer(2.0, hideShow, [r])
     t.start();


def resetApps():#spanum enq sax hnuc hnaravor e mnacac baner
    os.system('killall omxplayer 2>/dev/null')
    os.system('killall omxplayer.bin 2>/dev/null')




if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    
    launch = Launch()
    launch.initQML()
    client = mqtt.Client(name)
    client.connect("192.168.0.100",1883)
    #client.connect("192.168.2.2",1883)
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.on_message = lambda c, d, msg: launch.client_message.emit(msg)# ays masi shnorhiv a ashkhatel u pyqtsygnali. kareli a pordzel hanel classic durs, kam el hakarak@ mtcnel mej@
    launch.client_message.connect(on_message)

    resetApps()
    goStandby() 


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



    