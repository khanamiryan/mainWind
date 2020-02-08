import QtQuick 2.11
import QtQuick.Controls 2.4
import QtGraphicalEffects 1.0
import QtQuick.Layouts 1.11
import QtQuick.Window 2.3





ApplicationWindow {
    id: mainWindow
    property int step: 0
    property bool isWin: false
    // property var buttonAlreadyPressed: false
    visible: true
    visibility: "FullScreen"
    width:780 
    screen: Qt.application.screens[0]
    x: screen.virtualX
    y: screen.virtualY + screen.height - height
    height: 600
    
    
    flags: Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint 
    onStepChanged: {
        console.log(mainWindow.step)
        if(step===3)
            countdown.start()
    }
     onClosing: close.accepted = false
    MouseArea {
        anchors.fill: parent
        enabled: false
        cursorShape: Qt.BlankCursor
    }

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

//        Image {
//            id: image
//            x: 0
//            y: 0
//            fillMode: Image.PreserveAspectFit
//            source: "background.png"
//        }


        Image {
            id: animatedImage
            x: 8
            y: 8
            fillMode: Image.TileVertically
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.leftMargin: 0
            source: "input-block-background.png"
            anchors.topMargin: 0

            Text {
                id: subject
                objectName: "subject"
                x: 68
                y: 114
                width: 369
                height: 76
                color: "#ffffff"
                font.family: "GHEA Grapalat"

                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignBottom
                font.pixelSize: 25
                
            
                property string sText: ""
                // ### Important part ###
                text: sText
                Behavior on sText {
                    FadeAnimation {
                        target: subject
                    }
                }
                // ######################


            }

            Image {
                id: inputImage
                objectName: "inputImage"
                x: 83
                y: 209
                fillMode: Image.PreserveAspectFit
                source: "input.png"

                TextInput {

                    id: textInput
                    objectName: "textInput"
                    x: 48
                    y: 8
                    width: 237
                    height: 52
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
                    font.family: "Arial"
                    horizontalAlignment: Text.AlignHCenter
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
                        // textInput.text.
                        
                        textInput.text = textInput.text.replace(/\!/g, '1').replace(/\@/g, '2').replace(/\"/g, '2').replace(/\#/g, '3').replace(/\£/g, '3').replace(/\$/g, '4').replace(/\$/g, '4').replace(/\%/g, '5').replace(/\^/g, '6').replace(/\&/g, '7').replace(/\*/g, '8').replace(/\(/g, '9').replace(/\)/g, '0');
                        launch.textEdited(textInput.text)
                        //weaponCodeBlock.text = textInput.text
                    }

                }
            }


            states: [
                State{
                    name:"step1"
                    when: mainWindow.step===1
                    PropertyChanges {
                        target: weaponCodeBlock
                        stateVisible:true
                    }
                },
                State{
                    name:"step2"
                    when: mainWindow.step===2
                    PropertyChanges {
                        target: weaponCodeBlock
                        stateVisible:true
                    }
                    PropertyChanges {
                        target: coordinatesBlock
                        stateVisible:true
                    }
                },

                State {
                    name:"step3"
                    when: mainWindow.step===3||mainWindow.step===30
                    
                    PropertyChanges {
                        target: subject
                        y: 187
                        opacity: 1
                        scale:1
                        color: '#ffffff'
                        font.bold :true
                        lineHeight: 1.5 
                        

                    }
                    PropertyChanges {
                        target: inputImage
                        visible:false

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

                },
                Transition {

                    to: "step3"
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
                source: "coordinatner.png"


            }

            BlockItem {
                id: fireBlock
                objectName: "fireBlock"
                x: 200
                source: "Asset 3.png"
                text: ''
            

                CountDown{
                    id:countdown
                    seconds: 10
                    defaultSeconds: 10
                    onTriggert:{
                        buttonOrCountdown(false,true)
                    }
                }

            }

        }
    }
    
    function buttonOrCountdown(pressed,fromCountdown) {
            if (fromCountdown === undefined) fromCountdown = false
            if(pressed&&step==30){
                
                    subject.sText = "FATAL ERROR\nՏեղի է ունեցել սխալմունք"
                    isWin = false
            }
            
            if(step==3&&!isWin){
                if(!fromCountdown&&pressed&&countdown.seconds>0){
                    if((weaponCodeBlock.text.toUpperCase()=="GLC"||weaponCodeBlock.text.toUpperCase()=="AIL")&&coordinatesBlock.text=="163"){
                        subject.sText = "Այոոոո"
                        countdown.stop()
                        isWin = true
                    }
                    else{
                        subject.sText = "Տեղի ունեցավ սխալ:\nՄուտքագրեք ճիշտ տվյալներ\n և սեղմեք կարմիր կոճակը"
                        countdown.stop()
                        isWin = false
                    }
                }else{
                    subject.sText = "Տեղի ունեցավ սխալ:\nՄուտքագրեք ճիշտ տվյալներ\n և սեղմեք կարմիր կոճակը"//chen sexmel knopken
                    isWin = false
                }
            }
            

            launch.buttonPressFromQml(step,countdown.seconds,isWin)
            step = 0
    }
    Connections {
        target: launch

        // Обработчик сигнала 
        onTextEdit: {
            

            if(step==1)
                weaponCodeBlock.text = text
            else if(step==2)
                coordinatesBlock.text = text

        }
        onButtonPressed:{ 
            buttonOrCountdown(pressed)
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
