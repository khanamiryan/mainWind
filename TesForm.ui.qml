import QtQuick 2.13
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.0

Item {

    id: element

    antialiasing: true
    width: 750
    height: 500

    clip: false

    Image {
        id: image
        x: 0
        y: 0
        fillMode: Image.PreserveAspectFit
        source: "background.png"
    }

    AnimatedImage {
        id: animatedImage
        x: 8
        y: 8
        playing: true
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: 0
        source: "input-block.png"
        anchors.topMargin: 0

        Text {
            id: element1
            x: 68
            y: 96
            width: 369
            height: 103
            color: "#ffffff"
            text: 'downloader.filename'
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 30
        }

        TextInput {
            id: textInput
            x: 134
            y: 210
            width: 237
            height: 63
            color: "#ffffff"
            text: qsTr("Tex")
            font.bold: true
            font.italic: false
            font.underline: false
            font.strikeout: false
            font.preferShaping: true
            font.letterSpacing: 40
            renderType: Text.QtRendering
            activeFocusOnPress: true
            font.kerning: true
            font.family: "Arial"
            horizontalAlignment: Text.AlignRight
            padding: 3
            rightPadding: 2
            bottomPadding: 2
            leftPadding: 2
            topPadding: 2
            cursorVisible: false
            font.capitalization: Font.AllUppercase
            font.pixelSize: 50
        }
    }

    Image {
        id: image3
        x: 497
        y: 33
        fillMode: Image.PreserveAspectFit
        source: "Asset 1.png"

        Text {
            id: element3
            x: 74
            y: 34
            width: 149
            height: 29
            color: "#f3f2f2"
            text: qsTr("Text")
            horizontalAlignment: Text.AlignHCenter
            wrapMode: Text.WrapAnywhere
            font.pixelSize: 24
            styleColor: "#f7eeee"
            verticalAlignment: Text.AlignVCenter
            elide: Text.ElideMiddle
            font.capitalization: Font.AllUppercase
            font.weight: Font.Black

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    element3.color = Qt.rgba(Math.random(), Math.random(),
                                             Math.random(), 1)
                }
            }
            states: State {
                name: "moved"
                when: mouseArea.pressed
                PropertyChanges {
                    target: image3
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

    Image {
        id: image2
        x: 497
        y: 180
        fillMode: Image.PreserveAspectFit
        source: "Asset 2.png"

        Text {
            id: element2
            objectName: "element2"
            x: 74
            y: 34
            width: 149
            height: 29
            color: "#f3f2f2"
            text: 'downloader.filename'
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            wrapMode: Text.WrapAnywhere
            elide: Text.ElideMiddle
            font.weight: Font.Black
            font.capitalization: Font.AllUppercase
            styleColor: "#f7eeee"
            font.pixelSize: 25
        }
    }

    Image {
        id: image4
        objectName: "image4"
        x: 497
        y: 332
        Text {
            id: element4
            x: 74
            y: 34
            width: 149
            height: 29
            color: "#f3f2f2"
            text: qsTr("Text")
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
    }
    states: [
        State {
            name: "analog"
            when: element3.pressed
            PropertyChanges {
                target: element4
                color: "green"
                x: 200
            }
            PropertyChanges {
                target: dialLoader
                source: "tqml.qml"
            }
        },
        State {
            name: "digital"
            PropertyChanges {
                target: digitalButton
                color: "green"
            }
            PropertyChanges {
                target: dialLoader
                source: "qmlother.qml"
            }
        }
    ]
}
