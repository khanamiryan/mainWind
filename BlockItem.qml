import QtQuick 2.13
import QtQuick.Controls 2.13

Image {
    id: fireBlock
    objectName: "fireBlock"

    opacity: 0
    x: 200
    property bool stateVisible: false
    property alias text: label.text
    property alias label: label
    Text {
        id: label
        x: 74
        y: 34
        width: 149
        height: 29
        color: "#f3f2f2"
        text: ''// fireBlock.stateVisible ? "visible" : "hidden"
        horizontalAlignment: Text.AlignHCenter
        wrapMode: Text.WrapAnywhere
        font.pixelSize: 24
        styleColor: "#f7eeee"
        font.capitalization: Font.AllUppercase
        elide: Text.ElideMiddle
        verticalAlignment: Text.AlignVCenter
        font.weight: Font.Black
    }
    fillMode: Image.PreserveAspectFit
    source: "Asset 3.png"
    //        Behavior on opacity {
    //            NumberAnimation { duration: 300
    //                easing {
    //                    type: Easing.OutElastic
    //                    amplitude: 0.5
    //                    period: 2.5
    //                }
    //            }
    //        }
    //        Behavior on x {
    //            NumberAnimation { duration: 500
    //                easing {
    //                    type: Easing.OutElastic
    //                    amplitude: 0.5
    //                    period: 2.5
    //                }
    //            }
    //        }
//    MouseArea {
//        anchors.fill: parent
//        onReleased: {
//            fireBlock.stateVisible = false
//        }
//        onPressed: {
//            fireBlock.stateVisible = true
//        }
//    }

    states: [
        State {
            id: show
            name: "show"
            when: fireBlock.stateVisible
            PropertyChanges {
                target: fireBlock
                x: 0
                opacity: 1
            }
        },
        State {
            id: hide
            name: "hide"
            when: !fireBlock.stateVisible
            PropertyChanges {
                target: fireBlock

                opacity: 0
                x: 200
            }
        }
    ]

    transitions: [
        Transition {

            NumberAnimation {
                target: fireBlock
                properties: "x,opacity"
                duration: 1
                easing.type: Easing.InOutQuad
            }
        },
        Transition {
            from: "show"
            to: "hide"
            id: showTrans

          //  SequentialAnimation {

                NumberAnimation {
                    properties: "x,opacity"
                    duration: 600
                    easing.type: Easing.InOutQuad
                }
                // PropertyAnimation { target:fireBlock;property: "visible"; to:0; duration: 0;}
           // }
        },
        Transition {
            id: hideTrans
            from: "hide"
            to: "show"

            //SequentialAnimation {
                //PropertyAnimation {  target:fireBlock;properties: "visible"; to:1; duration: 0; }
                NumberAnimation {
                    properties: "x,opacity"
                    duration: 600
                    easing.type: Easing.InOutQuad
                }
           // }
        }
    ]
}
