
import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
print (sys.path)

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
    "molorakner":{"status":"standby"},
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

 
    
    

        
    if(topic.find("toServer/")==0):#status@ grum enq dictionaryi mej, vor imanananq verjin ekac status@
        dev = topic.replace("toServer/","")
        if(dev in devices and message in statuses):
          setStatus(dev,message) 
          return True 
        
    if(topic != "toServer/molorakner" ):
        print("topic is "+topic)
        print("message is \""+message+"\"")
    
    if(message=="go-step-2"):
        startStep2()
    if(message=="go-step-3"):
        startStep3()
    if(message=="go-step-4"):
        startStep4()
    if(message=="go-step-5"):
        startStep5()
    if(message=="go-step-6"):
        startStep6()    
    if(message=="go-step-7"):
        startStep7()
    if(message=="go-step-8"):
        startStep8()
    if(message=="go-winner"):
        winner()

        # print("step",newStatus)
        # print ("ssss")
        # stepfunc = message.replace("step-","")
        # newfunc = ("startStep"+stepfunc)
        # newfunc()

    if(message=="startGame" and not isStarted and step==False):#sksum enq xax@
        startGame()
    if(message=="startGameForce"):#sksum enq noric, amen depqum
        startGame()
    if(message=="WelcomeVideoEnded"): #step 1
        startStep2()

    # if(message=="FirstVideoEnded"):
    #     startStep2()

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
    if(step==8 and message=="5" and topic=="toServer/molorakner"):#?? stugel chisht em grel client@?
        winner()
    if(message=="WinnerVideoEnded"):
        winnerVideoEnded()


    
    if(message=="keyboardActive"):
        keyboardActive()
    if(message=="keyboardStopped"):#keyboard@ barcracel e
        keyboardStopped()
    

    


def printit():
  threading.Timer(5.0, printit).start()
  print("step - ", step)

printit()


def publish(module,message,device=toDevice):
    #print ("send",message,"to ", device+module)
    #if((message in statuses) and (module in devices)):
    setStatus(module,message)
    client.publish(device+module, message)

def getStatus(dev):
    return devices[dev]["status"]

def setStatus(dev,status):
    global devices
    if(status in statuses and dev in devices):
        #print("SetStauts", status, "to device", dev)
        devices[dev]["status"] = status
def resetGame():#mianum a amenaskzbum, erb uxxaki der chi sksel xax@
    global step, isStarted
    
    publish("ALL","finished")
    
    publish("mainDisplay", "resetBlocks") #0acnum enq glxavor ekrani cragir@

    publish("lazer","closeLAZER") #lazer@ anjatum enq
    publish("lazer","closeLUYS")#luyser@ miacnum enq
    publish("mainDisplay", "standby")

    publish("relener","down")#ijacnum enq klaviarutan
    isStarted=False
    step = 0

def startGame():
    global step, isStarted 
    isStarted=True
    step = 1
    
    print("starting the game")
    resetGame()
    #publish("mainDisplay","notStartVideo")## vorpeszi chmiana finished i videon
    publish("ALL","finished")

    publish("mainDisplay","startWelcomeVideo")


def startStep2():#arajin angam anjatvum sax
    global step
    step=2
    
    publish("ALL","turnedoff")
    publish("lazer","openLUYS")
    publish("luyser","standby")
    
    publish("mainDisplay","notStartVideo")
    publish("mainDisplay","turnedoff")
    publish("mainDisplay","startFirstVideo")
    
    
    

def startStep3(): #mianum en gndakner@ u larer@ verjapes sksum en askhatel
    global step
    step=3
    publish("lazer","closeLUYS")#mianum en senyaki luyser@
    time.sleep(0.1)#navsyaki, qani vor nuyn device in enq message uxarkum
    publish("lazer","standby")#mianum en senyaki luyser@
    
    publish("mainDisplay","startStep3Video")
    time.sleep(5.0) # 5 varkyan heto nor mianan 
    publish("balls3","standby")
    publish("larer","standby")
    publish("relener","openD3") #gndakner@ amenaaji darakum en, bacum enq
    #publish("balonner","standby")#???


def startStep4(): #todo es mas@ poxvum a, karchanum a
    global step
    step=4
    publish("mainPanel","standby")
    publish("leftPanel","standby")
    publish("rightPanel","standby")
    time.sleep(2)
    publish("mainDisplay","notStartVideo")
    publish("mainDisplay","standby")
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
    t = threading.Timer(150, startStep5Continue)##qani varkyan en xaxum
    t.start()

def startStep5Continue():#xax@ avartecin asuma, petq a zenqov kraken
    global step
    step=5
    publish("mainDisplay","startFirstWeaponUseVideo")
    time.sleep(4)
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
    print("step is 6")
    publish("relener","openD7")#cxi apparat@ miacaca, taqacaca,  miacnum enq cux@
    
    time.sleep(2)
    publish("relener","down") #navsyaki ijacnenq
    publish("lazer","openLUYS")#anjatum en senyaki luyser@
    
    t = threading.Timer(15, stopSmoke)##15 varkyanic cux@ anjatum enq
    t.start()
    publish("mainDisplay","startStep6Video")
    time.sleep(2)
    publish("lazer","openLAZER")#mianuma lazer@
    publish("mainDisplay","lazerTime")#mianuma lazer@, dra hamar ampulaner@ piti hatuk dzev linen
    publish("mainPanel","lazerTime")#mianuma lazer@, dra hamar ampulaner@ piti hatuk dzev linen
    

def startStep7():##videon mianuma, klaviatiuran barcranuma, erb iranq petq havaqen chisht kod@
    global step
    step=7
    publish("mainDisplay","startStep7Video")
    publish("lazer","closeLAZER")
    
    
    publish("relener","up")
    publish("mainPanel","keyboardActive")
    time.sleep(2)
    publish("lazer","closeLUYS")#anjatum en senyaki luyser@
    
    

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
    publish("lazer","closeLUYS")#miacnum en senyaki luyser@

def continueStep8():
    global step
    step=8
    publish("relener","openD1")#?
    time.sleep(0.1)
    publish("relener","openD2")#?
    publish("relener","openD5")
    publish("leftPanel","hidden")
    publish("molorakner","standby")##active??




def winner():#haxtecin
    global step
    step = 0
    publish("mainDisplay","startWinnerVideo") 
    publish("ALL","finished")

def winnerVideoEnded():
    publish("lazer","openDUR")
    time.sleep(0.1)
    publish("lazer","openDRSIDUR")
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
    print(sys.argv) 
    if(len(sys.argv)>1 and sys.argv[1]=="boot"):
        
        print("sleep from boot")
        time.sleep(15) 

    client = mqtt.Client("mainServer")
    #client.connect("192.168.0.100",1883)
    client.connect("127.0.0.1",1883)

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
