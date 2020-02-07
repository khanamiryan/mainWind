import vlc
import time
import sys
import platform

from PyQt5.QtWidgets import QApplication, QFrame,QMacCocoaViewContainer

Instance = vlc.Instance('--fullscreen')
player = Instance.media_player_new()



  
url = '/home/pi/Desktop/mainWind/videos/Step31.mp4'

Media = Instance.media_new(url)
player.set_media(Media)




player.play()
while True:
     pass