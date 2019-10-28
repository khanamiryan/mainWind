import QtQuick 2.13
import QtQuick.Controls 2.13

TesForm {


    transitions: [
        Transition {
            from: "*"
            to: "middleRight"
            NumberAnimation {
                properties: "x,y"
                easing.type: Easing.InOutQuad
                duration: 2000
            }
        },
        Transition {
            from: "*"
            to: "bottomLeft"
            NumberAnimation {
                properties: "x,y"
                easing.type: Easing.InOutQuad
                duration: 200
            }
        },
        //If any other rectangle is clicked, the icon will return
        //to the start position at a slow speed and bounce.
        Transition {
            from: "*"
            to: "*"
            NumberAnimation {
                easing.type: Easing.OutBounce
                properties: "x,y"
                duration: 4000
            }
        }
    ]

    Image {
        id: image3


        states: State {
            name: "moved"
            when: image3.pressed
            PropertyChanges {
                target: rect
                x: 50
                y: 50
            }
        }

        transitions: Transition {
            NumberAnimation {
                properties: "x,y"
                easing.type: Easing.InOutQuad
            }
        }
    }


}

/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
##^##*/
