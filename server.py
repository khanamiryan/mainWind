
import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
print (sys.path)

import threading
import time
from threading import Event, Thread


    

    
    

import paho.mqtt.client as mqtt

# This is the Subscriber
isStarted = False
client = mqtt.Client()

toDevice = "toDevice/"
balls3 = "balls3"
larer = "larer"
luyser = "luyser"
step = 0
step31 = False
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
otherDevices = ["relener"]

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
    global step31
    global isStarted
    global cancel_future_calls
    message = msg.payload.decode()
    topic = msg.topic

 
    
    

        
    if(topic.find("toServer/")==0):#status@ grum enq dictionaryi mej, vor imanananq verjin ekac status@
        dev = topic.replace("toServer/","")
        if(dev in devices and message in statuses):
          setStatus(dev,message) 
          return True 
        
    #if(topic != "toServer/molorakner" ):
    #    print("topic is "+topic)
    #    print("message is \""+message+"\"")
    
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

    if(message=="resetGame"):
        resetGame()
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
    if(step==3 and step31==False and getStatus("balls3")=="finished" and getStatus("larer")!="finished"):
        startStep32()
        step31 = True
    if(step==3 and step31==False and getStatus("balls3")!="finished" and getStatus("larer")=="finished"):
         
        startStep31()
        step31 = True

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
    #if(step==8 and  message=="Step8VideoEnded"):
        #continueStep8()##patmec, vor moloraker@ xarnvel en, petq banali ta, vor bacen, nayev taqun pahac@
    if(step==8 and message=="5" and topic=="toServer/molorakner"):#?? stugel chisht em grel client@?
        winner()
    if(topic=="toServer/molorakner"):
        publish("mainDisplay","molorakner-"+message)
        # print ("molorakner-"+message)
    if(message=="WinnerVideoEnded"):
        winnerVideoEnded()


    
    if(message=="keyboardLiftActive"):  
        keyboardLiftActive()
    if(message=="keyboardLiftStopped"):#keyboard@ barcracel e kam ijel
        keyboardLiftStopped()
    
    if(message=="rebootServer"):
        os.system('sudo shutdown -r now')

    if(message=="startSchedule"):
       luyseriBlinkStart()



    
    if(message=="stopSchedule"):
    
        luyseriBlinkStop()

 
    
    


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
    global step, isStarted, step31
    
    publish("ALL","finished")
    
    publish("mainDisplay", "resetBlocks") #0acnum enq glxavor ekrani cragir@

    publish("lazer","closeLAZER") #lazer@ anjatum enq
    publish("lazer","closeLUYS")#luyser@ miacnum enq

    publish("relener","closeD6")#cxi apparati anjatum
    publish("relener","closeD7")##anjatum enq cxi knopken
    
    #pakum enq drner@
    publish("relener","closeD3")
    publish("relener","closeD4")
    publish("relener","closeD5")
    
    publish("lazer","closeDUR")
    publish("lazer","closeDRSIDUR")

    publish("mainDisplay", "standby")

    publish("relener","down")#ijacnum enq klaviarutan
    publish("relener","switchoffKeyboard")#ijacnum enq klaviarutan
    
    luyseriBlinkStop()
    
    isStarted=False
    step = 0
    step31 = False

def startGame():
    global step, isStarted 
    isStarted=True
    step = 1
    
    print("starting the game")
    resetGame()
    #publish("mainDisplay","notStartVideo")## vorpeszi chmiana finished i videon
    #publish("mainDisplay","notStartVideo")
    publish("ALL","finished")

    publish("mainDisplay","startWelcomeVideo")
    publish("relener","openD6")#cxi apparati miacum


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

    publish("mainDisplay","startStep3Video")

    publish("lazer","closeLUYS")#mianum en senyaki luyser@
    #time.sleep(0.1)#navsyaki, qani vor nuyn device in enq message uxarkum
    publish("lazer","standby")#mianum en senyaki luyser@
    
    t = threading.Timer(5, startStep3Timer)##qani varkyan en xaxum
    t.start()
    
def startStep31():
    step=3
    publish("mainDisplay","startStep31Video")

def startStep32():
    step=3
    publish("mainDisplay","startStep32Video")

    #publish("balonner","standby")#???
def startStep3Timer():
    publish("balls3","standby")
    publish("larer","standby")
    d = threading.Timer(5, openD4)##qani varkyan en xaxum
    d.start()
    
def openD4():
    publish("relener","openD4") #gndakner@ amenaaji darakum en, bacum enq
def startStep4(): 
    global step
    step=4
    publish("mainDisplay","startStep4Video")#ayooo miacanq

    publish("mainPanel","standby")
    publish("leftPanel","standby")
    publish("rightPanel","standby")
    
    t = threading.Timer(2, startStep4Timer)##qani varkyan en xaxum
    t.start()
    
  
def startStep4Timer():
    publish("mainDisplay","notStartVideo")
    publish("mainDisplay","standby")
    publish("relener","openD6")#cxi apparati miacum w   w
    
    
    

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
    
    publish("mainDisplay","startEmulation")
    t = threading.Timer(150, startStep5Continue)##qani varkyan en xaxum
    t.start()

def startStep5Continue():#xax@ avartecin asuma, petq a zenqov kraken
    global step
    step=5
    publish("mainDisplay","startFirstWeaponUseVideo")
    
    
    t = threading.Timer(3, startStep5ContinueTimer)
    t.start()
    
    
def startStep5ContinueTimer():
    publish("mainDisplay","stopEmulation")
    return

def startFirstWeaponUse():
    global step
    step=5
    publish("mainDisplay","startFirstWeaponUse")

def stopSmoke():
    publish("relener","closeD7")##anjatum enq cxi knopken
    
def stopSmoke2():
    publish("relener","closeD6")##anjatum enq cxi apparat@

def startStep6():#petq a licqavoren zenq@
    global step
    step=6
    print("step is 6")
    publish("relener","openD7")#cxi apparat@ miacaca, taqacaca,  miacnum enq cux@
    
    
    publish("relener","down") #navsyaki ijacnenq
    publish("lazer","openLUYS")#anjatum en senyaki luyser@
    publish("lazer","openUV")
    
    t = threading.Timer(15, stopSmoke)##15 varkyanic cux@ anjatum enq
    
    t1 = threading.Timer(25, stopSmoke2)##25 varkyanic cuxi apparat@
    t.start()
    t1.start()
    publish("mainDisplay","startStep6Video")
    
    publish("lazer","openLAZER")#mianuma lazer@
    publish("mainDisplay","lazerTime")#mianuma lazer@, dra hamar ampulaner@ piti hatuk dzev linen
    publish("mainPanel","lazerTime")#mianuma lazer@, dra hamar ampulaner@ piti hatuk dzev linen
    publish("relener","openD3") #hayelineri darak@


    publish("mainPanel","turnedoff")
    publish("leftPanel","turnedoff")
    publish("rightPanel","turnedoff")
    publish("larer","turnedoff")
    publish("luyser","turnedoff")
    publish("balls3","turnedoff")
    

def startStep7():##videon mianuma, klaviatiuran barcranuma, erb iranq petq havaqen chisht kod@
    global step
    step=7
    publish("mainDisplay","startStep7Video")
    publish("lazer","closeLAZER")
    
    
    publish("relener","up")
    publish("mainPanel","keyboardLiftActive")
    
    t = threading.Timer(2, startStep7Timer)##qani varkyan en xaxum
    t.start()




    
def startStep7Timer():##todo anel, vor tarti 5 varkyan@ mek
    publish("lazer","closeLUYS")#mianum en senyaki luyser@
    
    
 
    return

    # publish("klaviatura","startturnedoff") #het qashenq klaviaturan
    # openDoor(1) #bacel 1 magnisov dur@
    # time.sleep(5)

def continueStep7():##petq a arden havaqen kod@
    global step
    step=7
    luyseriBlinkStart()
    
    publish("mainDisplay","startRealWeaponUse")

def startStep8():
    global step
    step=8

    publish("mainPanel","standby")
    publish("leftPanel","standby")
    publish("rightPanel","standby")
    publish("larer","finished")
    publish("luyser","finished")
    publish("balls3","finished")
    

    
    publish("lazer","closeUV")
    luyseriBlinkStop()
    publish("mainDisplay","startStep8Video")
    publish("relener","down")
    publish("mainPanel","keyboardLiftActive")
    publish("lazer","closeLUYS")#miacnum en senyaki luyser@
    t = threading.Timer(40, continueStep8)##qani varkyan en xaxum
    t.start()
    
    

def continueStep8():
    global step
    step=8
    #publish("relener","openD1")#?
    #time.sleep(0.1)
    #publish("relener","openD2")#?
    publish("relener","openD5")
    publish("leftPanel","hidden")
    publish("molorakner","standby")##active??
    return


def winner():#haxtecin
    global step
    step = 0
    publish("mainDisplay","startWinnerVideo") 

    t = threading.Timer(5, winnerTimer)##qani varkyan en xaxum
    t.start()
    publish("ALL","finished")
    
def winnerTimer():
    publish("lazer","openDUR")
    return


def winnerVideoEnded():
    publish("lazer","openDRSIDUR")
    resetGame()



def keyboardLiftActive():
    publish("mainPanel","keyboardLiftActive")
def keyboardLiftStopped():
    publish("mainPanel","keyboardLiftStopped")

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





##luyser@ tartelu hamar

def call_repeatedly(interval, func, *args):
    stopped = Event()
    def loop():
        while not stopped.wait(interval): # the first call is in `interval` secs
            func(*args)
    Thread(target=loop).start()    
    return stopped.set


luyseriblink = None
luyseriblinkstat = 0
def luyseriBlinkStart():
    global luyseriblink
    if(luyseriblink is not None):
            
            luyseriblink()  
    luyseriblink = call_repeatedly(7, luyserBlinkWork)

def luyseriBlinkStop():
    global luyseriblink
    if(luyseriblink is not None):
        luyseriblink()

    publish("lazer","closeLUYS")#miacnum enq senyaki luyser@

def luyserBlinkWork():
    global luyseriblinkstat
    if(luyseriblinkstat==0):
        publish("lazer","openLUYS")#anjatum en senyaki luyser@
    elif(luyseriblinkstat==1):
        publish("lazer","closeLUYS")#miacnum enq senyaki luyser@
    luyseriblinkstat = not luyseriblinkstat


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
