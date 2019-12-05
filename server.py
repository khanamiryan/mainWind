
import sys
import os
import threading
import time




import paho.mqtt.client as mqtt

# This is the Subscriber
isStarted = False
client = mqtt.Client()

toDevice = "toDevice/"
balls3 = "balls3"
larer = "larer"
luyser = "luyser"
step = 0;
statuses = ["turnedoff","standby","finished","failed","active"]
devices = {
    "balls3":{"status":"standby"},
    "larer":{"status":"standby"},
    "luyser":{"status":"standby"},
    "lazer":{"status":"standby"},
    "balonner":{"status":"standby"},
    "mainPanel":{"status":"standby"},
    "leftPanel":{"status":"standby"},
    "rightPanel":{"status":"standby"},
    "mainDisplay":{"status":"standby"},#todo texapoxel other devices

    # "element":{"status":"standby"}

    } #devices with last state
otherDevices = ["roomLights"]

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print ("Unexpected MQTT disconnection. Will auto-reconnect")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    for key in devices:
        client.subscribe("toServer/"+key)
        print("subscribe to "+ key)

    for otherDev in otherDevices:
        client.subscribe("toServer/"+otherDev)
        print("subscribe to "+ otherDev)

    client.subscribe("toServer")
    print("subscribe to "+ "toServer")

def on_message(client, userdata, msg):
    global step
    global isStarted
    message = msg.payload.decode()
    topic = msg.topic

    # print("topic is "+topic)
    # print("message is \""+message+"\"")
    
    
    if(topic.find("toServer/")==0):#status@ grum enq dictionaryi mej, vor imanananq verjin ekac status@
        dev = topic.replace("toServer/","")
        if(dev in devices and message in statuses):
          devices[dev]["status"] = message



    if(message=="startGame" and not isStarted and step==False):#sksum enq xax@
        startGame()
    if(message=="startGameForce"):#sksum enq noric, amen depqum
        startGame()
    if(message=="WelcomeVideoEnded"):
        firstTurnoffAll()

    if(message=="FirstVideoEnded"):
        
        startStep2()
    if(step==2 and getStatus("luyser")=="finished"):#haxtecin luyser@, ancnnen myus blokin   hin mnacac  and ((topic=="toServer/luyser" and message=="finished") or
        startStep3()
    if(step==3 and getStatus("balls3")=="finished" and getStatus("larer")=="finished"):
        startStep4()
    if(step==4 and message=="Step4VideoEnded"):#xosac, asec vor petqa payqaren demetrikusi dem, kraken ev ayln,
        startStep5()#mianuma emulacian (Step4 videoi mej )
    if(step==5 and  message=="FirstWeaponUseVideoEnded"):
        startFirstWeaponUse()
    if(step==5 and message=="FirstWeaponFailed"):##krakel en pchacela, piti stugenq, vor mi angam ga, dra hamar step@ poxum enq
        startStep6()
    if(step==6 and message=="zenqiActivationFinished"):#lazerov licqavorcin zenq@ chist, arden petq a havaqen kod@ chisht
        startStep7()
    if(step==7 and message=="Step7VideoEnded"):
        continueStep7()#jamanakna kod@ havaqelu
    if(step==7 and message=="RealWeaponUsedRight"):##chisht en havaqel kod@@, karelia gmpa mmpa
        startStep8()
    if(step==8 and  message=="Step8VideoEnded"):
        continueStep8()##patmec, vor moloraker@ xarnvel en, petq banali ta, vor bacen, nayev taqun pahac@
    if(step==8 and message=="5" and client=="toServer/molorakner"):#?? stugel chisht em grel client@?
        winner()
    if(message=="WinnerVideoEnded"):
        winnerVideoEnded()


    
    if(message=="keyboardActive"):
        keyboardActive()
    if(message=="keyboardStopped"):#keyboard@ barcracel e
        keyboardStopped()
    


    # if(step==4 and getStatus("element")=="failed"):#chi stacvum luyser@, ancnnen myus blokin
    #     startStep4Failed()
    # if(step==4 and getStatus("element")=="finished"):#haxtecin luyser@, ancnnen myus blokin
    #     startStep5()
    if(getStatus("klaviatura")=="finished"):#klaviaturan bardzracav
        klaviaturaActivationEnded()
    if(getStatus("klaviatura")=="turnedoff"):#anjatecinq klaviaturan, vor ijni
            klaviaturaDeActivationEnded()

    if(step==5 and message=="step5VideoEnded"):
        zenqiActivation1()
    if(step==5 and message=="zenqiActivation1Failed"):
        zenqiActivation1Failed()
    if(step==5 and message=="zenqiActivation1FailedVideoEnded"):
        zenqiActivation2()
    if(step==5 and message=="zenqiActivation2Finished"):#todo avelacnel mainDisplay finished kam nman ban
        startStep6()
        klaviaturaDeactivation()
    


def printit():
  threading.Timer(5.0, printit).start()
  print("step - ", step)

printit()


def publish(module,message,device=toDevice):
    print ("send",message,"to ", device+module)    
    client.publish(device+module, message)
def getStatus(dev):
    return devices[dev]["status"]

def resetGame():#mianum a amenaskzbum, erb uxxaki der chi sksel xax@
    global step, isStarted

    publish("ALL","finished")
    publish("mainDisplay", "resetBlocks")
    publish("lazer","closeLAZER")
    isStarted=False
    step = 0

def startGame():
    global step, isStarted 
    isStarted=True
    step = 1
    print("starting the game")
    publish("ALL","finished")
    publish("lazer","closeLAZER")
    time.sleep(2)
    publish("mainDisplay","startWelcomeVideo")

def firstTurnoffAll():#arajin angam anjatvum sax
    publish("ALL","turnedoff")
    time.sleep(5)
    publish("mainDisplay","startFirstVideo")
#skzbic luys@,

def startStep2():# mianum en en luyser vor petq a sarqen, vor askhati
    global step
    print("startStep2s")
    step=2
    publish("mainDisplay","startStep2Video")
    time.sleep(5)
    publish("luyser","standby")

def startStep3(): #mianum en gndakner@ u larer@ verjapes sksum en askhatel
    global step
    step=3
    publish("lazer","standby")#mianum en senyaki luyser@
    time.sleep(0.2)#navsyaki, qani vor nuyn device in enq message uxarkum
    publish("lazer","closeLUYS")#mianum en senyaki luyser@
    publish("mainDisplay","startStep3Video")
    time.sleep(5.0)
    publish("balls3","standby")
    publish("larer","standby")
    publish("balonner","standby")#???


def startStep4(): #todo es mas@ poxvum a, karchanum a
    global step
    step=4
    
    publish("mainDisplay","standby")
    publish("leftMonitor","standby")
    
    publish("mainPanel","standby")
    publish("leftPanel","standby")
    publish("rightPanel","standby")
    time.sleep(2)
    publish("mainDisplay","startStep4Video")#ayooo miacanq
    

# def startStep4second():#erb element@ texdrel en u zaryadka en talis
#     global step
#     time.sleep(0.1)

# def startStep4Failed():#erb chi stacvum lucen elementi xndir@
#     global step
#     publish("mainDisplay","startStep4FailedVideo")
#     time.sleep(1)



def startStep5():#erb petq e xax xaxan
    global step
    step=5
    publish("relener","openD6")#cxi apparati miacum
    publish("mainDisplay","startEmulation")
    t = threading.Timer(15, startStep5Continue)##qani varkyan en xaxum
    t.start()

def startStep5Continue():#xax@ avartecin asuma, petq a zenqov kraken
    global step
    step=5
    publish("mainDisplay","startFirstWeaponUseVideo")
    time.sleep(2)
    publish("mainDisplay","stopEmulation")

def startFirstWeaponUse():
    global step
    step=5
    publish("mainDisplay","startFirstWeaponUse")

def stopSmoke():
    publish("relener","closeD7")##anjatum enq cxi apparatner@
    publish("relener","closeD6")

def startStep6():#petq a licqavoren zenq@
    global step
    step=6

    publish("relener","openD7")#cxi apparat@ miacaca, taqacaca,  miacnum enq cux@

    time.sleep(5)

    publish("lazer","openLUYS")#anjatum en senyaki luyser@
    
    t = threading.Timer(15, stopSmoke)##15 varkyanic cux@ anjatum enq
    t.start()
    publish("mainDisplay","startStep6Video")
    time.sleep(2)
    publish("lazer","openLAZER")#mianuma lazer@
    publish("lazer","lazerTime")#mianuma lazer@, dra hamar ampulaner@ piti hatuk dzev linen

def startStep7():##videon mianuma, klaviatiuran barcranuma, erb iranq petq havaqen chisht kod@
    global step
    step=7
    publish("mainDisplay","startStep7Video")
    publish("lazer","closeLAZER")
    publish("relener","up")
    publish("mainPanel","keyboardActive")
    # publish("klaviatura","startturnedoff") #het qashenq klaviaturan
    # openDoor(1) #bacel 1 magnisov dur@
    # time.sleep(5)

def continueStep7():##petq a arden havaqen kod@
    global step
    step=7
    publish("mainDisplay","startRealWeaponUse")

def startStep8():
    global step
    step=8
    publish("mainDisplay","startStep8Video")
    publish("relener","down")
    publish("mainPanel","keyboardActive")

def continueStep8():
    global step
    step=8
    publish("relener","openD1")
    time.sleep(0.1)
    publish("relener","openD2")
    publish("leftPanel","hidden")
    publish("molorakner","standby")##active??




def winner():#haxtecin
    publish("mainDisplay","startWinnerVideo")
    publish("ALL","finished")

def winnerVideoEnded():
    publish("lazer","openDUR")
    time.sleep(0.1)
    publish("lazer","openDrsiDUR")
    time.sleep(5)    
    resetGame()



def keyboardActive():
    publish("mainPanel","keyboardActive")
def keyboardStopped():
    publish("mainPanel","keyboardStopped")

# def startStep5():#erb petq e havaqen zenqi kod@ arajin angam
#     step=5
    
#     time.sleep(5)
#     publish("mainPanel","klaviaturaActivation")
#     publish("klaviatura","active")

def klaviaturaActivationEnded():
    global step
    publish("mainPanel","active")

def zenqiActivation1():#zenq@ aktivacnum en, bayc pchanum a
    global step
    time.sleep(5)
    publish("mainDisplay","startZenqiActivation1")

def zenqiActivation1Failed():
    global step
    publish("roomLights","turnedoff")
    publish("mainDisplay","startZenqiActivation1FailedVideo")

#mtacel stex piti mtcnenq zenqi aktivaciayi lazeri pah@, karelia, erb lcvi, ira koxmi paneli luysn el lcvi, sirun klini


def zenqiActivation2():#zenq@ aktivacnum en, es angam, piti enqan anen, stacvi
    time.sleep(5)
    publish("mainDisplay","startZenqiActivation2")




def openDoor(doorID):
    publish("doors",doorID+"OFF") #bacel  magnisov dur@ (anjatel magnis@)

def closeDoor(doorID):
    publish("doors",doorID+"ON") #Pakel  magnisov dur@ (miacnel magnis@)

def main_loop():
    while 1:
      time.sleep(0.1)




if __name__ == '__main__':
    client = mqtt.Client("mainServer")
    client.connect("192.168.0.100",1883,60)

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.loop_start()
    resetGame()
    try:
        main_loop()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)


    sys.exit()
