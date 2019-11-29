#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/test")

def on_message(client, userdata, msg):
  if msg.payload.decode() == "Hello world!":
    print("Yes!")
    client.disconnect()

client = mqtt.Client()
client.connect("192.168.2.6",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()



if __name__ == '__main__':


    app = QApplication(sys.argv)

    #downloader = Downloader('https://cdimage.debian.org/debian-cd/current/armhf/iso-cd/debian-10.1.0-armhf-xfce-CD-1.iso')
    view = QQmlApplicationEngine()


    launch = Launch(view);



    print ("bob2")

    # Объект QQuickView, в который грузится UI для отображения

    #view = QtDeclarative.QDeclarativeView()
   # view.rootContext().setContextProperty("downloader", downloader)
    view.rootContext().setContextProperty("launch", launch)




    #view.setResizeMode(QQuickView.SizeRootObjectToView)
    view.load(QUrl('qml.qml'))

    launch.initQML()
    launch.step1()
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
