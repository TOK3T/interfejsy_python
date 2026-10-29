import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Basic
import QtQuick.Layouts
import QtQuick.Window

ApplicationWindow {
    id: root
    visible: true
    //visibility: Window.FullScreen
    width: 475
    height: 600
    minimumWidth: 450
    minimumHeight: 540
    color: "#d2d5d5"
    title: "System sterowania Growbox"

    ScrollView {
        id: scrollView
        anchors.fill: parent
        clip: true
        contentWidth: availableWidth

        ColumnLayout {
            width: scrollView.availableWidth
            spacing: 10

            Label {
                Layout.fillWidth: true
                Layout.topMargin: 12
                text: "--- ODCZYTY ---"
                font.family: "Consolas"
                font.pixelSize: 25
                font.weight: Font.DemiBold
                horizontalAlignment: Text.AlignHCenter
                color: "#2c2f2f"
            }

            Label {
                Layout.fillWidth: true
                text: "Temperatura: " + backend.temperatura.toFixed(1) + " °C"
                font.family: "Consolas"
                font.pixelSize: 18
                font.weight: Font.DemiBold
                horizontalAlignment: Text.AlignHCenter
                color: "#2c2f2f"
            }

            Label {
                Layout.fillWidth: true
                text: "Wilgotność: " + backend.wilgotnosc.toFixed(1) + " %"
                font.family: "Consolas"
                font.pixelSize: 18
                font.weight: Font.DemiBold
                horizontalAlignment: Text.AlignHCenter
                color: "#2c2f2f"
            }

            Label {
                Layout.fillWidth: true
                text: "Wilgotność gleby: " + backend.wilgotnoscGleby + " %"
                font.family: "Consolas"
                font.pixelSize: 18
                font.weight: Font.DemiBold
                horizontalAlignment: Text.AlignHCenter
                color: "#2c2f2f"
            }

            Label {
                Layout.fillWidth: true
                text: "Poziom światła: " + backend.poziomSwiatla
                font.family: "Consolas"
                font.pixelSize: 18
                font.weight: Font.DemiBold
                horizontalAlignment: Text.AlignHCenter
                color: "#2c2f2f"
            }

            Label {
                Layout.fillWidth: true
                text: "Stan wody: " + backend.stanWody
                font.family: "Consolas"
                font.pixelSize: 18
                font.weight: Font.DemiBold
                horizontalAlignment: Text.AlignHCenter
                color: "#2c2f2f"
            }

            Label {
                Layout.fillWidth: true
                text: "Stan dnia: " + backend.stanDnia + " | Tryb LED: " + backend.tryb
                font.family: "Consolas"
                font.pixelSize: 18
                font.weight: Font.DemiBold
                horizontalAlignment: Text.AlignHCenter
                color: "#2c2f2f"
            }

            Label {
                Layout.fillWidth: true
                Layout.topMargin: 12
                text: "--- Sterowanie ---"
                font.family: "Consolas"
                font.pixelSize: 25
                font.weight: Font.DemiBold
                horizontalAlignment: Text.AlignHCenter
                color: "#2c2f2f"
            }
            Row {
                Layout.alignment: Qt.AlignHCenter
                spacing: 10

                Button {
                    id: output1
                    width: 150
                    height: 60
                    hoverEnabled: true
                    text: "LIGHT: " + backend.stan1
                    palette.buttonText: "#ffffff"
                    font.pixelSize: 14
                    font.family: "Consolas"
                    font.weight: Font.DemiBold
                    onClicked: backend.przelaczWyjscie1()
                    background: Rectangle {
                        radius: 8
                        color: output1.down ? "#aab0b0"
                            : output1.hovered ? "#868e8e"
                            : "#6c7474"
                        border.color: "#454a4a"
                        border.width: 2
                    }
                }

                Button {
                    id: output2
                    width: 150
                    height: 60
                    hoverEnabled: true
                    text: "Heater: " + backend.stan2
                    palette.buttonText: "#ffffff"
                    font.pixelSize: 14
                    font.family: "Consolas"
                    font.weight: Font.DemiBold
                    onClicked: backend.przelaczWyjscie2()
                    background: Rectangle {
                        radius: 8
                        color: output2.down ? "#aab0b0"
                            : output2.hovered ? "#868e8e"
                            : "#6c7474"
                        border.color: "#454a4a"
                        border.width: 2
                    }
                }

            }

            RowLayout {
                spacing: 12
                Layout.alignment: Qt.AlignHCenter

                Label {
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignVCenter
                    text: "Fan 1 (PWM): " + backend.wartosc1
                    color: "#2c2f2f"
                    font.pixelSize: 14
                    font.family: "Consolas"
                    font.weight: Font.DemiBold
                    horizontalAlignment: Text.AlignHCenter
                }

                Slider {
                    Layout.fillWidth: true
                    Layout.leftMargin: 20
                    Layout.rightMargin: 20
                    Layout.bottomMargin: 12
                    from: 0
                    to: 255
                    stepSize: 1
                    value: backend.wartosc1
                    onMoved: backend.ustawWartosc1(Math.round(value))
                }

                Item { //Wiatrak 1 - obiekt/animacja
                    width: 72
                    height: 72
                    Layout.alignment: Qt.AlignVCenter

                    Item {
                        id: rotor1
                        anchors.fill: parent

                        Repeater { //Śmigła duże
                            model: 7

                            Rectangle {
                                width: 10
                                height: 30
                                radius: 7
                                x: (rotor1.width - width) / 2
                                y: rotor1.height / 2 - height
                                rotation: index * 52
                                transformOrigin: Item.Bottom
                                color: "#2c2f2f"
                            }
                        }

                        Repeater { //Mniejszy cień w śmigle
                            model: 7

                            Rectangle {
                                width: 3
                                height: 27
                                radius: 7
                                x: (rotor1.width - width) / 2
                                y: rotor1.height / 2 - height
                                rotation: index * 52
                                transformOrigin: Item.Bottom
                                color: "#696969"
                            }
                        }

                        Rectangle { //Środek
                            width: 14
                            height: 14
                            radius: 7
                            anchors.centerIn: parent
                            color: "#6c7474"
                        }

                        NumberAnimation on rotation {
                            from: 0
                            to: 360
                            duration: 800
                            loops: Animation.Infinite
                            running: backend.wartosc1 > 0
                        }
                    }

                    Rectangle {
                        anchors.fill: parent
                        radius: width / 2
                        color: "transparent"
                        border.color: "#6c7474"
                        border.width: 3
                    }
                }
            }

            RowLayout {
                spacing: 12
                Layout.alignment: Qt.AlignHCenter

                Label {
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignVCenter
                    text: "Fan 2 (PWM): " + backend.wartosc2
                    horizontalAlignment: Text.AlignHCenter
                    color: "#2c2f2f"
                    font.pixelSize: 14
                    font.family: "Consolas"
                    font.weight: Font.DemiBold
                }

                Slider {
                    Layout.fillWidth: true
                    Layout.leftMargin: 20
                    Layout.rightMargin: 20
                    from: 0
                    to: 255
                    stepSize: 1
                    value: backend.wartosc2
                    onMoved: backend.ustawWartosc2(Math.round(value))
                }


                Item {
                    width: 72
                    height: 72
                    Layout.alignment: Qt.AlignVCenter

                    Item {
                        id: rotor2
                        anchors.fill: parent

                        Repeater {
                            model: 7

                            Rectangle {
                                width: 10
                                height: 30
                                radius: 7
                                x: (rotor2.width - width) / 2
                                y: rotor2.height / 2 - height
                                rotation: index * 52
                                transformOrigin: Item.Bottom
                                color: "#2c2f2f"
                            }
                        }

                        Repeater {
                            model: 7

                            Rectangle {
                                width: 3
                                height: 27
                                radius: 7
                                x: (rotor2.width - width) / 2
                                y: rotor2.height / 2 - height
                                rotation: index * 52
                                transformOrigin: Item.Bottom
                                color: "#696969"
                            }
                        }

                        Rectangle {
                            width: 14
                            height: 14
                            radius: 7
                            anchors.centerIn: parent
                            color: "#6c7474"
                        }

                        NumberAnimation on rotation {
                            from: 0
                            to: 360
                            duration: 800
                            loops: Animation.Infinite
                            running: backend.wartosc2 > 0
                        }
                    }

                    Rectangle {
                        anchors.fill: parent
                        radius: width / 2
                        color: "transparent"
                        border.color: "#6c7474"
                        border.width: 3
                    }
                }
            }

        }
    }
}
