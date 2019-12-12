
# This Python file uses the following encoding: utf-8
import sys
import time
import os
import subprocess 
import threading

import platform

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

if(platform.system()=="Linux"):
    import pyautogui
    from inputs import get_gamepad
    from omxplayer.player import OMXPlayer
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO23
    GPIO.setup(24, GPIO.OUT)  #LED to GPIO24


import paho.mqtt.client as mqtt

from urllib.request import urlopen
from PyQt5.QtCore import QObject, QUrl, Qt, pyqtProperty, pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType, QQmlEngine, QQmlComponent
from PyQt5 import QtCore, QtGui
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import QQmlContext



from pathlib import Path






# if__name__ == "__main__":
#     pass
import sys
# Класс QUrl предоставляет удобный интерфейс для работы с Urls
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget
# Класс QQuickView предоставляет возможность отображать QML файлы.
from PyQt5.QtQuick import QQuickView
 
redirectory = "/home/pi/"


global status
status = "standby"
def on_connect(client, userdata, flags, rc):#
    print("Connected with result code "+str(rc))
    client.subscribe("toDevice/mainDisplay")
    client.subscribe("toDevice/ALL")
    client.publish("toServer/mainDisplay", payload='hello', qos=0, retain=False)
    client.publish("toServer/mainDisplay", payload=status, qos=0, retain=False)



def publish(message,device="toServer/mainDisplay"):
    client.publish(device, message)


def on_message(msg):
    
    global status#globali poxaren urish ban mtacel


    newStatus = msg.payload.decode()
    
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
        startVideo("Welcome",False)        

    if(newStatus=="startFirstVideo"):
        startVideo("First",False)      

    # if(newStatus=="startStep2Video"):
    #     startVideo("Step2")

    if(newStatus=="startStep3Video"):
        startVideo("Step3")
    if(newStatus=="startStep4Video"):
        startVideo("Step4")#sranic heto emulaciana mianym
    
    if(newStatus == "startFirstWeaponUseVideo"):#arajin angam zenqi havaqelna, vor traquma zenq@
        startVideo("FirstWeaponUse",False,minimal_position=0)
    if(newStatus == "startFirstWeaponUse"):#arajin angam zenqi havaqelna, vor traquma zenq@        
        launch.step3ForFail()
        stopMainVideo()
    if(newStatus=="startStep6Video"):##lazerov petqa licqavoren, asuma vor sxal en krakel, ruchnoy piti licqavoren anen, petqa mi qani angam asi es mek@
        startVideo("Step6")
        launch.hide()
    if(newStatus=="startStep7Video"):##video, voric heto arden piti havaqen kod@
        startVideo("Step7")

    if(newStatus=="startRealWeaponUse" or newStatus=="startZenqiActivation1"):
        launch.step1()
        time.sleep(2)
        stopMainVideo()##petq en?

    if(newStatus=="startStep8Video"):##video, voric heto arden piti havaqen kod@
        startVideo("Step8")
    
    if(newStatus=="startWinnerVideo"):##video, voric heto arden piti havaqen kod@
        startVideo("Winner")


    if(newStatus=="killVideo"):
        stopMainVideo()
        
    if(newStatus=="startEmulation"):

        startEmulation()
    if(newStatus=="stopEmulation"):
        killEmulation()
        
    
    if(newStatus == "openEmulationMenu"):
       
        openEmulationMenu()

    if(newStatus=="volumeDown"):
        volumeDown()
    if(newStatus=="volumeUp"):
        volumeUp()
        
        

name = "mainDisplay"




omxp = None
omxp2 = None
omxp3 = None
dbusNames = ['org.mpris.MediaPlayer2.omxplayer1','org.mpris.MediaPlayer2.omxplayer3']
players = [omxp, omxp3]
activePlayer = 0
lastActivePlayer = 0
playerVolume = 1.0

p = None
omxp_thread = {}
omxp_thread[0] = threading.Thread()
omxp_thread[1] = threading.Thread()
emulationstate = False


standby_video = "Standby"


def volumeUp():
    global playerVolume
    if(playerVolume<1):
        playerVolume+=0.05
        players[activePlayer].set_volume(playerVolume)
        print(playerVolume)
    
    


def volumeDown():
    global playerVolume
    if(playerVolume>0):
        playerVolume-=0.05
        players[activePlayer].set_volume(playerVolume)
        print(playerVolume)
    
    



def goStandby():
    global status
    #here will be player
    status = "standby"
    startSecondMonitor()
    startVideo("Standby")
    startSecondMonitor("standby-secondary")

def goTurnedOff():
    global status
    #here is video, that onnection problems
    status = "turnedoff"
    startSecondMonitor("turnedoff-secondary")
    startVideo("Turnedoff-standby")
    



def player_position_thread(publish_text = "",minimal_position = 3,standby_video="",called_player=0):
    global omxp
    global omxp3
    global players
    global activePlayer
    
    b = 1 
    while b==1:
        # try omxp
        
        try:
            if(activePlayer is not called_player):
                b=0
            if(players[called_player].duration()-players[called_player].position()< minimal_position):#qani varkyana mnacel avartin
                publish(publish_text)
                print("publish_text ",publish_text)
                if(standby_video):
                    print("startVideo from thread",standby_video)
                    startVideo(standby_video,True)
                b=0
            
                
                
        except Exception as err: 
            print("execption")
            if(standby_video):
                print("startVideo from threadddd",standby_video)
            
            print("called player", called_player)
            print("publish_text ",publish_text)
            print("****err*****", str(err))
            return "not ok"
        
            



# def exitVideoEvent(event_code,movie_path,player):
#     print('exit', event_code)
#     ##tt.cancel()
#     if(event_code==0):
#         omxp_thread[player].cancel()
#     #if(event_code==0):
#      #   startVideo(movie_path)





def startVideo(movie_path="Standby",loop=True,options="",minimal_position=3):
    global omxp
    global omxp3
    global players
    global omxp_thread
    global activePlayer
    global lastActivePlayer
    global playerVolume
    
    if(platform.system()=="Linux"):
        
        VIDEO_PATH = Path("./videos/"+movie_path+".mp4")
        if(not os.path.exists(VIDEO_PATH)):
            print("file", VIDEO_PATH, "not exists")
            return "notok"
        thread_args={"publish_text" : movie_path+"VideoEnded"}

        if(os.path.exists("./videos/"+movie_path+"-Standby.mp4")):
            thread_args["standby_video"]=movie_path+"-Standby"
            loop=False##guce heto hanenq

        vargs='--aspect-mode fill --display 2 --no-osd --no-keys -b'

        if(loop==True):
            vargs+=' --loop'
        
        if(lastActivePlayer == activePlayer):
            activePlayer = 0 #arajin angamna
        else:
            activePlayer = int(not activePlayer)
        
        lastActivePlayer = int(not activePlayer)
        
        players[activePlayer] = OMXPlayer(VIDEO_PATH,  
                    dbus_name=dbusNames[activePlayer],args=vargs)

        
        # print("player ",activePlayer,"is activated")
        # print("lastActivePlayer is ",lastActivePlayer)
        thread_args["called_player"]=activePlayer
        if(minimal_position):
            thread_args["minimal_position"] = minimal_position
        players[activePlayer].pause()    


        if(players[lastActivePlayer] is not None):
            print("players last active",players[lastActivePlayer],"going to be killed")
            time.sleep(0.5)
            try:
                players[lastActivePlayer].stop()
                omxp_thread[lastActivePlayer].join()
                print("player ",lastActivePlayer,"is killed")
            except Exception as err: 
                print(err)    
        players[activePlayer].play()
        players[activePlayer].set_volume(playerVolume)
        print(playerVolume)
    

        if(emulationstate==True):
            killEmulation()
           
            
            # omxp.load(VIDEO_PATH,args=vargs)
            
            
        
            
            
        
        #print(thread_args)


       # omxp_thread[activePlayer] = threading.Timer(players[activePlayer].duration()-3,timer_video, kwargs=thread_args)
        #omxp_thread[activePlayer].start()
        #print("movie_path",movie_path)
        #players[activePlayer].exitEvent += lambda _, exit_code: exitVideoEvent(exit_code,movie_path,activePlayer)

        omxp_thread[activePlayer] = threading.Thread(target=player_position_thread, kwargs=thread_args )
    
        omxp_thread[activePlayer].start()  
        #omxp_thread[activePlayer].join()  
           
        
        # if(omxp_thread[lastActivePlayer] and omxp_thread[lastActivePlayer].is_alive()):
        #     omxp_thread[lastActivePlayer].join()
        #omxp.mute() #heto hanel
        return players[activePlayer]

    return False

def startSecondMonitor(movie_path="standby-secondary",loop=True):
    global omxp2 
    
    if(platform.system()=="Linux"):
        VIDEO_PATH = Path("./videos/"+movie_path+".mp4")
        args='--aspect-mode fill --display 7 --no-osd --no-keys -b -o alsa'
        if(loop==True):
            args+=' --loop'
        if(omxp2 is None):
            omxp2 = OMXPlayer(VIDEO_PATH,
                    dbus_name='org.mpris.MediaPlayer2.omxplayer2',args=args)
        else:
            omxp2.load(VIDEO_PATH)
        
        #omxp2.mute()
        
        return omxp2
    
    return False 


def openEmulationMenu():
    pyautogui.hotkey('tab', 'w',interval=0.1)
    
    


def stopMainVideo():
    global players
    global activePlayer

    try:
        if(players[activePlayer] is not None):
            players[activePlayer].stop()
    except Exception as err: 
        print ("stopMainVideo error", err)
        return "notok "

def startEmulation():
    global p
    global emulationstate
    
    killEmulation()
    
    p=subprocess.Popen('/opt/retropie/emulators/retroarch/bin/retroarch -L /opt/retropie/libretrocores/lr-snes9x2010/snes9x2010_libretro.so --config /opt/retropie/configs/snes/retroarch.cfg "/home/pi/RetroPie/roms/snes/Space Megaforce (USA).sfc" --appendconfig /dev/shm/retroarch.cfg',shell=True)
    emulationstate = True

    time.sleep(2)
    launch.hide()

    stopMainVideo()
    
    

    
    #askhatuma

def killEmulation():
    global emulationstate
    if(emulationstate == True):
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
        self.buttonState = False

        button_t = threading.Thread(target=self.button_thread, args=())    
        button_t.start()
    

        gampead_t = threading.Thread(target=self.gamepad_thread, args=())
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
                    
    def button_thread(self):
    
        try:
            while True:
                self.buttonState = not GPIO.input(23)
                if self.buttonState == True:
                    self.buttonPressed.emit(self.buttonState)
                    GPIO.output(24, True)
                    time.sleep(0.2)
                else:
                    GPIO.output(24, False)
                    
        except Exception as err:
            print("err",err)
            GPIO.cleanup()

    # слот
    @pyqtSlot(str)
    def textEdited(self, text):#stex piti stugvi iravichak@
        self.textEdit.emit(text, self.step)
        if(self.step == 1 and len(text)==3):
            
            if(text.upper()=="GLC"):##nayev mecatar
                QtCore.QTimer.singleShot(500, self.step2)
            else:
                self.subject.sText = "Տեղի ունեցավ սխալ:\nՄուտքագրեք ճիշտ տվյալներ\n և սեղմեք կարմիր կոճակը"
                QtCore.QTimer.singleShot(3000, self.step1)

        elif(self.step==2 and len(text)==3):          
            if(text=="163"):
                QtCore.QTimer.singleShot(500, self.step3)
            else:
                self.subject.sText = "Տեղի ունեցավ սխալ:\nՄուտքագրեք ճիշտ տվյալներ\n և սեղմեք կարմիր կոճակը"
                QtCore.QTimer.singleShot(3000, self.step2)

        elif(self.step==3):
            text = ''
        
      #..... 

    @pyqtSlot(int,int, bool)
    def buttonPressFromQml(self,qmlStep,qmlSeconds,isWin): ##from qml.qml buttonOrCountdown function
        print("qmlstep",qmlStep)
        print ("isWin",isWin)
        if(qmlStep==30 and isWin==False): #sexmel en knopkayin arajin krakelu jamanak
            publish("FirstWeaponFailed")
            startVideo()
            QtCore.QTimer.singleShot(500, self.hide)
  
        if(qmlStep==3 and isWin==False):
            publish("RealWeaponUsedFailed")
            QtCore.QTimer.singleShot(5000, self.step1)
            
        elif(qmlStep==3 and isWin==True): 
            publish("RealWeaponUsedRight")
            QtCore.QTimer.singleShot(5000, self.hide)

                    
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
        print("going to ","step3ForFail","function")
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
    print(sys.argv)
    if(len(sys.argv)>1 and sys.argv[1]=="boot"):
        time.sleep(15)




    app = QApplication(sys.argv)

    
    launch = Launch()
    launch.initQML()
    client = mqtt.Client(name)
    #client.connect("192.168.0.100",1883)
    client.connect("127.0.0.1",1883)
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.on_message = lambda c, d, msg: launch.client_message.emit(msg)# ays masi shnorhiv a ashkhatel u pyqtsygnali. kareli a pordzel hanel classic durs, kam el hakarak@ mtcnel mej@
    launch.client_message.connect(on_message)
    stopMainVideo()
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



    