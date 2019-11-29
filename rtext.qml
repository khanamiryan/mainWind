import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.3

ApplicationWindow{
        property var randtext: "Hello world!"
        visible:true
        width:940
        height:680

        id:root

        title: "markdwon editor"

        function setText(t)
        {
            randtext = t
        }

        Rectangle{

            Text{
                id:exampleId
                text:randtext
            }
        }
}