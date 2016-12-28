from PyQt5.QtCore import pyqtSignal, pyqtSlot, pyqtProperty, QObject, QSize
from PyQt5.QtQuick import QQuickItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QOpenGLShader, QOpenGLShaderProgram
from OpenGL.GL import *


class SquircleRenderer(QObject):
	def __init__ ( self, parent = None ):
		super().__init__(parent)
		self._shader_program = None
		self._t = 0.0
		self._viewport_size = QSize()
		self._window = None

	def set_viewport_size ( self, viewport_size ):
		self._viewport_size = viewport_size

	def set_t ( self, t ):
		self._t = t

	def set_window ( self, window ):
		self._window = window

	@pyqtSlot()
	def paint ( self ):
		if self._shader_program is None:
			self._shader_program = QOpenGLShaderProgram()
			self._shader_program.addShaderFromSourceCode(QOpenGLShader.Vertex,
			                                             "attribute highp vec4 vertices;"
			                                             "varying highp vec2 coords;"
			                                             "void main() {"
			                                             "    gl_Position = vertices;"
			                                             "    coords = vertices.xy;"
			                                             "}")

			self._shader_program.addShaderFromSourceCode(QOpenGLShader.Fragment,
			                                             "uniform lowp float t;"
			                                             "varying highp vec2 coords;"
			                                             "void main() {"
			                                             "    lowp float i = 1. - (pow(abs(coords.x), 4.) + pow(abs(coords.y), 4.));"
			                                             "    i = smoothstep(t - 0.8, t + 0.8, i);"
			                                             "    i = floor(i * 20.) / 20.;"
			                                             "    gl_FragColor = vec4(coords * .5 + .5, i, i);"
			                                             "}")

			self._shader_program.bindAttributeLocation('vertices', 0)
			self._shader_program.link()

		self._shader_program.bind()
		self._shader_program.enableAttributeArray(0)

		values = [
			(-1.0, -1.0),
			(1.0, -1.0),
			(-1.0, 1.0),
			(1.0, 1.0)
		]

		self._shader_program.setAttributeArray(0, values)
		self._shader_program.setUniformValue('t', self._t)

		glViewport(0, 0, self._viewport_size.width(), self._viewport_size.height())

		glDisable(GL_DEPTH_TEST)

		glClearColor(0, 0, 0, 1)
		glClear(GL_COLOR_BUFFER_BIT)

		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE)

		glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
		self._shader_program.disableAttributeArray(0)
		self._shader_program.release()

		self._window.resetOpenGLState()


class Squircle(QQuickItem):
	t_changed = pyqtSignal(name = 't_changed')

	def __init__ ( self, t = 0.0, parent = None ):
		super().__init__(parent)
		# self._renderer = None
		self._t = t
		self._renderer = None
		self.windowChanged.connect(self.onWindowChanged)

	# @pyqtSlot(QQuickView, name = 'onWindowChanged')
	def onWindowChanged ( self, window ):
		self.window().beforeSynchronizing.connect(self.sync, type = Qt.DirectConnection)
		self.window().setClearBeforeRendering(False)

	@pyqtSlot()
	def sync ( self ):
		if self._renderer is None:
			self._renderer = SquircleRenderer()
			self.window().beforeRendering.connect(self._renderer.paint, type = Qt.DirectConnection)
		self._renderer.set_viewport_size(self.window().size() * self.window().devicePixelRatio())
		self._renderer.set_t(self._t)
		self._renderer.set_window(self.window())

	@pyqtProperty('float', notify = t_changed)
	def t ( self ):
		return self._t

	@t.setter
	def t ( self, t ):
		if t == self._t:
			return
		self._t = t
		self.t_changed.emit()

		if self.window():
			self.window().update()
