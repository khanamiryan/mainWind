import vlc
import time
import sys
import platform

from PyQt5.QtWidgets import QApplication, QFrame,QMacCocoaViewContainer

Instance = vlc.Instance('--fullscreen')
player = Instance.media_player_new()



  
url = '/Users/Ashot/Desktop/galaktikus/valerian.mp4'

Media = Instance.media_new(url)
player.set_media(Media)


import sys
vlcApp =QApplication(sys.argv)
if platform.system() == "Darwin": # for MacOS
    videoframe = QMacCocoaViewContainer(0)
else:
    videoframe = QFrame()

videoframe.resize(700,700)
videoframe.show()
player.set_nsobject(int(videoframe.winId()))
player.play()
while True:
     pass