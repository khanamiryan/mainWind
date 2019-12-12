function Timer() {
    return Qt.createQmlObject("import QtQuick 2.0; Timer {}", root);
}

timer = new Timer();
timer.interval = 1000;
timer.repeat = true;
timer.triggered.connect(function () {
    print("I'm triggered once every second");
})

timer.start();