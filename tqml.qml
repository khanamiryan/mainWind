
import QtQuick 2.0
import QtQuick.Controls 1.0
ApplicationWindow{
    id: mainWindow
    visible: true
    width: 750
    height: 500

Rectangle {
    id: root
    width: 400; height: width

    Column {
        spacing: 20
        Repeater {
            model: ["one", "two", "three", "four"]
            Button {
                text: modelData
                onClicked: rect.state = modelData
            }
        }
    }

    Rectangle {
        id: rect
        x: 200; y: 0
        width: 60; height: width
        color: "red"

        state: "one"
        states: [
            State { name: "one" },
            State { name: "two" },
            State { name: "three" },
            State { name: "four" }
        ]
        NumberAnimation { id: na1; target: rect; property: "y"; to: 200 }
        NumberAnimation { id: na2; target: rect; property: "y"; to: 0 }
        transitions:
            Transition {
                 from: "two"; to: "three";
                 //whatever animation you have for this
            }
            //and obviously any other transitions you may have

            //any transition you don't specify will do this:
            Transition {
                 from: "*"; to: "*";
                 ParallelAnimation {
                     NumberAnimation { properties: "x,y"; duration: 500; easing.type: Easing.InOutQuad }
                     ColorAnimation { duration: 500 }
                 }
         }

    }
}
}
