import platform

import sys
import time
import os
import subprocess 
import threading
name = "mainDisplay"
from omxplayer.player import OMXPlayer

omxp = None
omxp2 = None
omxp3 = None
dbusNames = ['org.mpris.MediaPlayer2.omxplayer1','org.mpris.MediaPlayer2.omxplayer3']
players = [omxp, omxp3]
activePlayer = 0
lastActivePlayer = 0
playerVolume = 1

import paho.mqtt.client as mqtt


p = None
omxp_thread = {}
omxp_thread[0] = threading.Thread()
omxp_thread[1] = threading.Thread()
emulationstate = False

notStartVideo = False ##sa nra hamar e, vor erb vor petq chi inch hajord videon miacnel, bayc status@ petqa, asenq standby gnaluc ev ayln

standby_video = "Standby"

lang  = "arm"

mainPath = "./videos/"+lang+"/"

from pathlib import Path

def startVideo(movie_path="Standby",loop=True,options="",minimal_position=3,isMusic=False):
    global omxp
    global omxp3
    global players
    global omxp_thread
    global activePlayer
    global lastActivePlayer
    global playerVolume
    global notStartVideo
    global mainPath

    if(notStartVideo==True):##ete activacrel enq, vor hajord videon chenq cuyc talu, mi angam chenq cuyc talis u gnum enq araj
        notStartVideo = False
        return 
    vargs=""    
    fileType = "mp4"
    
    if(platform.system()=="Linux"):
        if(isMusic==True):
            fileType="mp3"
        VIDEO_PATH = Path(mainPath + movie_path+"."+fileType)
        if(not os.path.exists(VIDEO_PATH)):
            print("file", VIDEO_PATH, "not exists")
            return "notok"
        thread_args={"publish_text" : movie_path+"VideoEnded"}

        if(os.path.exists(mainPath + movie_path+"-Standby."+fileType)):
            thread_args["standby_video"]=movie_path+"-Standby"
            loop=False##guce heto hanenq

     
        if(isMusic==False):
            vargs+=' -o local  --aspect-mode fill --display 2 --no-osd --no-keys -b  '
        else:
            vargs+=' -o local '
            
        if(loop==True):
            vargs+=' --loop '
        
        if(lastActivePlayer == activePlayer):
            activePlayer = 0 #arajin angamna
        else:
            activePlayer = int(not activePlayer)
         
        lastActivePlayer = int(not activePlayer)
        
        players[activePlayer] = OMXPlayer(VIDEO_PATH,  
                    dbus_name=dbusNames[activePlayer],args=vargs)

        players[activePlayer].file_name = movie_path

        
        thread_args["called_player"]=activePlayer
        if(minimal_position):
            thread_args["minimal_position"] = minimal_position
        players[activePlayer].pause()    


        if(players[lastActivePlayer] is not None):
        
            try:
                players[lastActivePlayer].stop()
                omxp_thread[lastActivePlayer].b = 1
                print("player ",lastActivePlayer,"is killed"," filename is", players[lastActivePlayer].get_filename())
            except Exception as err: 
                print("lastactive player error",err)    
        try:                
            players[activePlayer].play()
            players[activePlayer].set_volume(playerVolume)
            
            # print(playerVolume)
        except Exception as err:
            print("activeplayer err",err)

    

        if(emulationstate==True):
            killEmulation()
        
        if(isMusic==False): 
            omxp_thread[activePlayer] = threading.Thread(target=player_position_thread, kwargs=thread_args )
        
            omxp_thread[activePlayer].start()  

       
        return players[activePlayer]

    return False


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
                print('aborting actieplayer thread',publish_text)
                b=0

            if(players[called_player].duration()-players[called_player].position()< minimal_position):#qani varkyana mnacel avartin
              #  publish(publish_text)
                print("publish_text ",publish_text)
                if(standby_video):
                    print("startVideo from thread",standby_video)
                    startVideo(standby_video,True)
                print('aborting actieplayer thread after 2s')
                b=0
            
                
                
        except Exception as err: 
            print("execption")
            if(standby_video):
                print("startVideo from threadddd",standby_video)
            
            print("called player", called_player)
            print("publish_text ",publish_text)
            print("****error video thread*****", str(err))
            return "not ok"
    return False
            

if __name__ == '__main__':
   
    startVideo()   

    try:
        while 1:
            time.sleep(0.1)
    except KeyboardInterrupt:
        
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)
    sys.exit()