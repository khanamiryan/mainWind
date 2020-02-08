import vlc
import time
import sys
import platform

from PyQt5.QtWidgets import QApplication, QFrame,QMacCocoaViewContainer

Instance = vlc.Instance('--fullscreen')
player = Instance.media_player_new()



  
<<<<<<< HEAD
url = '/Users/Ashot/Desktop/galaktikus/valerian.mp4'
=======
url = '/home/pi/Desktop/mainWind/videos/Step31.mp4'
>>>>>>> 196904b4c917e7487a9fb661af1adf064592689b

Media = Instance.media_new(url)
player.set_media(Media)


<<<<<<< HEAD
import sys
vlcApp =QApplication(sys.argv)
if platform.system() == "Darwin": # for MacOS
    videoframe = QMacCocoaViewContainer(0)
else:
    videoframe = QFrame()

videoframe.resize(700,700)
videoframe.show()
player.set_nsobject(int(videoframe.winId()))
=======


>>>>>>> 196904b4c917e7487a9fb661af1adf064592689b
player.play()
while True:
     pass