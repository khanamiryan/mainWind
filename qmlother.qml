import QtQuick 2.13
import QtQuick.Controls 2.13

MainForm {
    id: window
    visible: true
    //visibility: "FullScreen"
    width: 750
    height: 500
    title: qsTr("Stack")

    Component.onCompleted: {
        setX(Screen.width / 2 - width / 2);
        setY(Screen.height / 2 - height / 2);
    }

    Item {

        id: element

        antialiasing: true
        width: 750
        height: 500
        clip: false
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
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
                x: 145
                y: 155
                width: 210
                height: 33
                text: qsTr("Text")
                font.pixelSize: 12
            }

            TextEdit {
                id: textEdit
                x: 134
                y: 210
                width: 237
                height: 64
                text: qsTr("Text Edit")
                font.pixelSize: 12
            }
        }
        states: [
            State {
                name: "State3"

                PropertyChanges {
                    target: image
                    x: 30
                }

                PropertyChanges {
                    target: animatedImage
                    x: 300
                    height: 300
                }

                PropertyChanges {
                    target: textEdit
                    x: 30
                }
            }
        ]
    }
    header: ToolBar {
        contentHeight: toolButton.implicitHeight

        ToolButton {
            id: toolButton
            text: stackView.depth > 1 ? "\u25C0" : "\u2630"
            font.pixelSize: Qt.application.font.pixelSize * 1.6
            onClicked: {
                if (stackView.depth > 1) {
                    stackView.pop()
                } else {
                    drawer.open()
                }
            }
        }

        Label {
            text: stackView.currentItem.title
            anchors.centerIn: parent
        }
    }


}
