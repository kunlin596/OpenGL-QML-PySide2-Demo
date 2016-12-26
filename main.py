from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import qmlRegisterType, QQmlApplicationEngine
from PyQt5.QtCore import QUrl
from PyQt5.QtQuick import QQuickView

from squircle import Squircle

import sys

if __name__ == '__main__':
	qmlRegisterType(Squircle, "OpenGLUnderQML", 1, 0, "Squircle")

	app = QGuiApplication(sys.argv)
	view = QQuickView()
	view.setSource(QUrl('main.qml'))
	view.show()

	sys.exit(app.exec())
