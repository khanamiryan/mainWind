import QtQuick 2.3
import QtQuick.Window 2.3
//import "../shared" as Shared


     
        Window {
            id: cluster
            title: "Cluster Display"
            height: 720
            width: 1920
            visible: "FullScreen"
            screen: Qt.application.screens[0]

            color: "black"

            


            Component.onCompleted: {
                WindowManager.registerCompositorView(cluster)
                cluster.show()
            }
        
    }


 
        
        Window {
            id: cluster1
            title: "Cluster Display"
            height: 720
            width: 1920
            visible: "FullScreen"
            screen: Qt.application.screens[1]

            color: "black"

            

            Component.onCompleted: {
                WindowManager.registerCompositorView(cluster1)
                cluster1.show()
            }
        
    }
   