import os
import sys
from pathlib import Path

import PySide6
import connect
from backend import Backend
from PySide6.QtCore import QUrl, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

if os.name == "nt":
    _qt_dll_directory = os.add_dll_directory(
        str(Path(PySide6.__file__).resolve().parent)
    )


def main():
    app = QGuiApplication(sys.argv)
    connect.start_odbior()

    backend = Backend()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("backend", backend)
    qml_file = Path(__file__).resolve().with_name("main.qml")
    engine.load(QUrl.fromLocalFile(str(qml_file)))
    if not engine.rootObjects():
        print(f"Nie udało się załadować interfejsu: {qml_file}", file=sys.stderr)
        return 1

    timer = QTimer(backend)
    timer.timeout.connect(backend.odswiezDane)
    timer.start(500)
    backend.odswiezDane()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())