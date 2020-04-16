from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QAction, QWidget
from board import Board
from PyQt5.QtGui import QKeySequence

class MainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		self.setObjectName("MainWindow")
		self.setFixedSize(800, 640)
		self.setupUi(self)

	def setupUi(self, MainWindow):
		self.centralwidget = QtWidgets.QWidget(self)

		self.board = Board(self)
		
		self.comboBox = QtWidgets.QComboBox(self.centralwidget)
		self.comboBox.setGeometry(QtCore.QRect(630, 30, 141, 61))
		self.comboBox.setObjectName("comboBox")
		self.comboBox.addItem("1")
		self.comboBox.currentIndexChanged.connect(self.change_curve)
		self.comboBoxCounter = 1

		self.label = QtWidgets.QLabel(self.centralwidget)
		self.label.setGeometry(QtCore.QRect(650, 91, 60, 24))
		self.label.setObjectName("label")

		self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
		self.spinBox.setGeometry(QtCore.QRect(720, 91, 48, 24))
		self.spinBox.setMinimum(1)
		self.spinBox.setMaximum(10)
		self.spinBox.setObjectName("spinBox")
		self.spinBox.valueChanged.connect(self.set_power)
		self.spinBox.setFocusPolicy(QtCore.Qt.NoFocus)

		self.label2 = QtWidgets.QLabel(self.centralwidget)
		self.label2.setGeometry(QtCore.QRect(650, 121, 60, 24))
		self.label2.setObjectName("label2")

		self.spinBox2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
		self.spinBox2.setGeometry(QtCore.QRect(720, 121, 48, 24))
		self.spinBox2.setMinimum(0.1)
		self.spinBox2.setMaximum(10)
		self.spinBox2.setObjectName("spinBox2")
		self.spinBox2.setSingleStep(0.1)
		self.spinBox2.setDecimals(1)
		self.spinBox2.setValue(1.0)
		self.spinBox2.valueChanged.connect(self.set_weight)
		self.spinBox2.setFocusPolicy(QtCore.Qt.NoFocus)

		self.newCurveButton = QtWidgets.QPushButton(self.centralwidget)
		self.newCurveButton.setGeometry(QtCore.QRect(630, 330, 141, 61))
		self.newCurveButton.setObjectName("newCurveButton")
		self.newCurveButton.clicked.connect(self.add_curve)

		self.deleteCurveButton = QtWidgets.QPushButton(self.centralwidget)
		self.deleteCurveButton.setGeometry(QtCore.QRect(630, 400, 141, 61))
		self.deleteCurveButton.setObjectName("deleteCurveButton")
		self.deleteCurveButton.clicked.connect(self.delete_curve)
		MainWindow.setCentralWidget(self.centralwidget)

		menubar = self.menuBar()
		delAction = QAction('Delete last', self)
		delAction.setShortcut('Ctrl+A')
		delAction.setShortcutContext(QtCore.Qt.ApplicationShortcut)
		self.centralwidget.addAction(delAction)
		self.board.addAction(delAction)
		delAction.triggered.connect(self.board.delete_last_point)

		menu = menubar.addMenu('Menu')
		menu.addAction(delAction)
		menubar.setVisible(True)
		menubar.show()

		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.newCurveButton.setText(_translate("MainWindow", "New curve"))
		self.deleteCurveButton.setText(_translate("MainWindow", "Delete curve"))
		self.label.setText(_translate("MainWindow", "Order"))
		self.label2.setText(_translate("MainWindow", "Weight"))

	def add_curve(self):
		self.board.add_curve()
		self.comboBoxCounter += 1
		self.comboBox.addItem(str(self.comboBoxCounter))
		self.comboBox.setCurrentIndex(self.comboBoxCounter - 1)
		self.spinBox.setValue(1)

	def delete_curve(self):
		self.board.delete_curve()
		if self.comboBoxCounter > 1:
			self.comboBox.removeItem(self.comboBox.currentIndex())
			self.comboBoxCounter -= 1
			self.comboBox.setCurrentIndex(self.comboBoxCounter - 1)
	
	def change_curve(self, i):
		self.board.change_curve(i)

	def set_power(self):
		self.board.set_power(self.spinBox.value())

	def set_weight(self):
		self.board.set_weight(self.spinBox2.value())

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	
	MainWindow = MainWindow()
	MainWindow.show()

	sys.exit(app.exec_())

	
