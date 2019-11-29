import QtQuick 2.0


Item {
    id: countDown
    signal triggert
    property int defaultSeconds: 3
    property int seconds: defaultSeconds





    function faceToPlayer1() { rotation = 0 }
    function faceToPlayer2() { rotation = 180 }


    BlockItemText{
        id: countImg
        text: (innerTimer.running && countDown.seconds > 0) ? ""+countDown.seconds : ""

    }

    Timer {
        id: innerTimer
        repeat: true
        interval: 1000
        onTriggered: {
            countDown.seconds--;
            if (countDown.seconds == 0) {
                running = false;
                countDown.seconds = countDown.defaultSeconds
                countDown.opacity = 0
                countDown.triggert()
            }
        }
    }

    Behavior on opacity {
        PropertyAnimation { duration: 200 }
    }

    function start() {
        seconds = defaultSeconds
        opacity = 1;
        innerTimer.start();
    }

    function stop() {
        opacity = 0;
        innerTimer.stop();
    }
}
