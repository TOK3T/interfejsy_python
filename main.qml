import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root
    visible: true
    width: 380
    height: 600
    minimumWidth: 340
    minimumHeight: 540
    title: "Panel Czujników i Sterowania"

    ScrollView {
        anchors.fill: parent
        clip: true

        ColumnLayout {
            width: parent.width
            spacing: 8

            Label {
                Layout.fillWidth: true
                Layout.topMargin: 12
                text: "--- ODCZYTY Z PICO WH ---"
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
            }

            Label {
                Layout.leftMargin: 20
                text: "Temperatura: " + backend.temperatura.toFixed(1) + " °C"
            }

            Label {
                Layout.leftMargin: 20
                text: "Wilgotność: " + backend.wilgotnosc.toFixed(1) + " %"
            }

            Label {
                Layout.leftMargin: 20
                text: "Wilgotność gleby: " + backend.wilgotnoscGleby + " %"
            }

            Label {
                Layout.leftMargin: 20
                text: "Poziom światła: " + backend.poziomSwiatla
            }

            Label {
                Layout.leftMargin: 20
                text: "Stan wody: " + backend.stanWody
            }

            Label {
                Layout.leftMargin: 20
                text: "Stan dnia: " + backend.stanDnia + " | Tryb LED: " + backend.tryb
            }

            Label {
                Layout.fillWidth: true
                Layout.topMargin: 12
                text: "--- STEROWANIE PICO ---"
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
            }

            Button {
                Layout.alignment: Qt.AlignHCenter
                Layout.preferredWidth: 220
                text: "Wyjście 1: " + backend.stan1
                onClicked: backend.przelaczWyjscie1()
            }

            Button {
                Layout.alignment: Qt.AlignHCenter
                Layout.preferredWidth: 220
                text: "Wyjście 2: " + backend.stan2
                onClicked: backend.przelaczWyjscie2()
            }

            Label {
                Layout.leftMargin: 20
                Layout.topMargin: 8
                text: "Suwak 1 (0-255): " + backend.wartosc1
            }

            Slider {
                Layout.fillWidth: true
                Layout.leftMargin: 20
                Layout.rightMargin: 20
                from: 0
                to: 255
                stepSize: 1
                value: backend.wartosc1
                onMoved: backend.ustawWartosc1(Math.round(value))
            }

            Label {
                Layout.leftMargin: 20
                text: "Suwak 2 (0-255): " + backend.wartosc2
            }

            Slider {
                Layout.fillWidth: true
                Layout.leftMargin: 20
                Layout.rightMargin: 20
                Layout.bottomMargin: 12
                from: 0
                to: 255
                stepSize: 1
                value: backend.wartosc2
                onMoved: backend.ustawWartosc2(Math.round(value))
            }
        }
    }
}
