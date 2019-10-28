import QtQuick 2.13
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.0
import QtQuick.Layouts 1.11

ApplicationWindow {
    id: mainWindow
    property int step: 0
    visible: true
    width: 750
    height: 500

    //flags: Qt.FramelessWindowHint // Disable window frame

    // Declare properties that will store the position of the mouse cursor
    Image {
        id: imag2
        x: 0
        y: 0
        width: 750
        height: 500
        fillMode: Image.Stretch
        anchors.fill: parent
        source: "background.png"
    }
    property int previousX
    property int previousY

    Item {

        id: element

        antialiasing: true
        width: 750
        height: 500
        anchors.centerIn: parent
        clip: false

        Image {
            id: image
            x: 0
            y: 0
            fillMode: Image.PreserveAspectFit
            source: "background.png"
        }


        Image {
            id: animatedImage
            x: 8
            y: 8
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.leftMargin: 0
            source: "input-block.png"
            anchors.topMargin: 0

            Text {
                id: subject
                objectName: "subject"
                x: 68
                y: 80
                width: 369
                height: 95
                color: "#ffffff"
                font.family: "GHEA Grapalat"

                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.pixelSize: 25


            }

            TextInput {

                id: textInput
                objectName: "textInput"
                x: 134
                y: 210
                width: 237
                height: 63
                color: "#ffffff"
                text: ''
                font.bold: true
                font.italic: false
                font.underline: false
                font.strikeout: false
                font.preferShaping: true
                font.letterSpacing: 40
                renderType: Text.QtRendering
                activeFocusOnPress: true
                font.kerning: true
                font.family: "GHEA Grapalat"
                horizontalAlignment: Text.AlignCenter
                padding: 3
                rightPadding: 2
                bottomPadding: 2
                leftPadding: 2
                topPadding: 2
                cursorVisible: false

                font.capitalization: Font.AllUppercase
                font.pixelSize: 50
                maximumLength:3
                onTextEdited:{
                    launch.textEdited(textInput.text)
                    //weaponCodeBlock.text = textInput.text
                }

            }

            states: [
                State {

                    when: mainWindow.step===3
                    PropertyChanges {
                        target: textInput

                        opacity: 0
                    }
                    PropertyChanges {
                        target: subject
                        y: 192
                        opacity: 1
                        scale:1
                    }
                }

            ]
            transitions: [
                Transition {

                    reversible: true
                    NumberAnimation {

                        properties: "y,opacity"
                        duration: 400

                    }
                    SequentialAnimation{

                    loops: Animation.Infinite
                    ScaleAnimator {
                           target: subject;
                           from: 1;
                           to: 1.1;
                            easing.type: Easing.OutCirc
                           duration: 500


                       }
                    ScaleAnimator {
                           target: subject;
                           from: 1.1;
                           to: 1;
                            easing.type: Easing.OutCirc
                           duration: 500


                       }
                    }
                }
            ]

        }
        ColumnLayout {
            x: 497

            height: parent.height

            BlockItem {
                id: weaponCodeBlock
                objectName: "weaponCodeBlock"
                x: 200
                source: "Asset 1.png"


            }

            BlockItem {
                id: coordinatesBlock
                objectName: "coordinatesBlock"
                x: 200
                source: "Asset 2.png"


            }

            BlockItem {
                id: fireBlock
                objectName: "fireBlock"
                x: 200
                source: "Asset 3.png"
                text: mainWindow.step

            }

        }
    }
    Connections {
        target: launch

        // Обработчик сигнала сложения
        onTextEdit: {
            // sum было задано через arguments=['sum']
            if(step==1)
                weaponCodeBlock.text = text
            else if(step==2)
                coordinatesBlock.text = text

        }

    }
    //    Connections{
    //        target: launch
    //        onStart: {

    //        }

    //        onVolumesignal:{
    //            if (fireBlock.stateVisible){
    //                Controller.stateVol=true
    //                animation.start();
    //                console.log("state of controller :", Controller.stateVol)
    //            } else if (!fireBlock.stateVisible){
    //                animation.stop();
    //                 Controller.stateVol=false
    //                console.log("state", Controller.stateVol)
    //            }
    //          }
    //      }
}
