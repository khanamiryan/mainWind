
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
    "balonner":{"status":"standby"},
    "mainDisplay":{"status":"standby"},#todo texapoxel other devices

    "element":{"status":"standby"}

    } #devices with last state
otherDevices = ["mainPanel","leftPanel","rightPanel","klaviatura","roomLights","doors"]

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

    message = msg.payload.decode()
    topic = msg.topic

    print("topic is "+topic)
    print("message is \""+message+"\"")

    if(topic.find("toServer/")==0):#status@ grum enq dictionaryi mej, vor imanananq verjin ekac status@
        dev = topic.replace("toServer/","")
        if(dev in devices and message in statuses):
          devices[dev]["status"] = message



    if(message=="startGame" and not isStarted and step==False):#sksum enq xax@
        startGame()
    if(message=="startGameForce"):#sksum enq noric, amen depqum
        startGame()
    if(message=="welcomeVideoEnded"):
        firstTurnoffAll()
    if(isStarted and step==1  and message=="firstVideoEnded"):
        startStep2()
    if(step==2 and getStatus("luyser")=="finished"):#haxtecin luyser@, ancnnen myus blokin   hin mnacac  and ((topic=="toServer/luyser" and message=="finished") or
        startStep3()
    if(step==3 and getStatus("balls3")=="finished" and getStatus("larer")=="finished"):
        startStep4()
    if(step==4 and getStatus("element")=="failed"):#chi stacvum luyser@, ancnnen myus blokin
        startStep4Failed()
    if(step==4 and getStatus("element")=="finished"):#haxtecin luyser@, ancnnen myus blokin
        startStep5()
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



def publish(module,message,device=toDevice):

    client.publish(device+module, message)
def getStatus(dev):
    return devices[dev]["status"]

def resetGame():#mianum a amenaskzbum, erb uxxaki der chi sksel xax@
    publish("ALL","standby")
    isStarted=False
    step = 0

def startGame():
    isStarted=True
    step = 1
    print("starting the game")
    publish("ALL","standby")
    time.sleep(5)
    publish("mainDisplay","startWelcomeVideo")

def firstTurnoffAll():#arajin angam anjatvum sax

    publish("ALL","turnedoff")
    time.sleep(5)
    publish("mainDisplay","startFirstVideo")

#skzbic luys@,

def startStep2():# mianum en en luyser vor petq a sarqen, vor askhati
    step=2
    publish("mainDisplay","startStep2Video")
    time.sleep(5)
    publish("luyser","standby")

def startStep3(): #mianum en gndakner@ u larer@ verjapes sksum en askhatel
    step=3
    publish("roomLights","standby")#mianum en senyaki luyser@
    publish("mainDisplay","startStep3Video")
    time.sleep(5)
    publish("balls3","standby")
    publish("larer","standby")
    publish("balonner","standby")


def startStep4(): #todo es mas@ poxvum a, karchanum a
    step=4
    publish("mainDisplay","startStep4Video")
    time.sleep(5)
    publish("element","standby")

def startStep4second():#erb element@ texdrel en u zaryadka en talis
    time.sleep(0.1)

def startStep4Failed():#erb chi stacvum lucen elementi xndir@
    publish("mainDisplay","startStep4FailedVideo")
    time.sleep(1)


def startStep5():#erb petq e havaqen zenqi kod@ arajin angam
    step=5
    publish("mainDisplay","startStep5Video")
    publish("leftMonitor","active")
    publish("rightMonitor","active")
    publish("mainPanel","active")
    publish("leftPanel","active")
    publish("rightPanel","active")
    time.sleep(5)
    publish("mainPanel","klaviaturaActivation")
    publish("klaviatura","active")

def klaviaturaActivationEnded():
    publish("mainPanel","active")

def zenqiActivation1():#zenq@ aktivacnum en, bayc pchanum a
    time.sleep(5)
    publish("mainDisplay","startZenqiActivation1")

def zenqiActivation1Failed():
    publish("roomLights","turnedoff")
    publish("mainDisplay","startZenqiActivation1FailedVideo")

#mtacel stex piti mtcnenq zenqi aktivaciayi lazeri pah@, karelia, erb lcvi, ira koxmi paneli luysn el lcvi, sirun klini


def zenqiActivation2():#zenq@ aktivacnum en, es angam, piti enqan anen, stacvi
    time.sleep(5)
    publish("mainDisplay","startZenqiActivation2")


def startStep6():#krakel en, haxtel en, mnuma molorakner@ dzen
    step=6
    publish("mainDisplay","startStep6Video")
    publish("klaviatura","startturnedoff") #het qashenq klaviaturan
    openDoor(1) #bacel 1 magnisov dur@
    time.sleep(5)


def openDoor(doorID):
    publish("doors",doorID+"OFF") #bacel  magnisov dur@ (anjatel magnis@)

def closeDoor(doorID):
    publish("doors",doorID+"ON") #Pakel  magnisov dur@ (miacnel magnis@)

def main_loop():
    while 1:
      time.sleep(0.1)




if __name__ == '__main__':
    client = mqtt.Client("mainServer")
    client.connect("192.168.2.2",1883,60)

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
