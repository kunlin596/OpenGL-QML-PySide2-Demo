from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import qmlRegisterType, QQmlApplicationEngine
from PySide2.QtCore import QUrl
from PySide2.QtQuick import QQuickView
from squircle import Squircle

import sys

if __name__ == '__main__':
    qmlRegisterType(Squircle, "OpenGLUnderQML", 1, 0, "Squircle")

    app = QGuiApplication(sys.argv)
    view = QQuickView()
    view.setSource(QUrl('main.qml'))
    view.show()

    sys.exit(app.exec_())
