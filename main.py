# -*- coding: utf-8 -*-
import sys
import Calculation
from MtMplCanv import *
from un import *

from PyQt5 import QtWidgets
import numpy as np
# Импортируем наш интерфейс из файла
#from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from tabwidg import *
from numpy import float64


class Window(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.sec_win = None
        self.fig = Figure()
        self.canvas = MtMplCanv(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.companovka_for_mpl = QtWidgets.QVBoxLayout(self.widget)
        self.companovka_for_mpl.addWidget(self.canvas)
        self.companovka_for_mpl.addWidget(self.toolbar)
        self.pushButton.clicked.connect(self.MyFunction)
    # при нажатии на кнопку

    def MyFunction(self):
        if str(self.comboBox.currentText()) == 'Test':
            self.textBrowser.setText("du/dx = -2.5*u")
        if str(self.comboBox.currentText()) == 'Main1':
            self.textBrowser.setText(
                "du/dx =  u^2 * ln(x + 1) / (x^2 + 1) + u - (u^3) * sin(10 * x)")
        if str(self.comboBox.currentText()) == 'Main2':
            self.textBrowser.setText(
                "du/dx =  u^2 * ln(x + 1) / (x^2 + 1) + u - (u^3) * sin(10 * x)")
        n = int(self.textEdit.toPlainText())
        u0 = float64(self.textEdit_4.toPlainText())
        h = float64(self.textEdit_5.toPlainText())
        x0 = float64(self.textEdit_2.toPlainText())
        eps = float64(self.textEdit_6.toPlainText())
        border = float64(self.textEdit_7.toPlainText())
        a = float64(self.textEdit_3.toPlainText())
        b = float64(self.textEdit_8.toPlainText())

        u10 = float64(self.textEdit_9.toPlainText())
        u20 = float64(self.textEdit_10.toPlainText())

        limx = float64(self.textEdit_11.toPlainText())
        lim1 = float64(self.textEdit_12.toPlainText())
        lim2 = float64(self.textEdit_13.toPlainText())
        step1 = float64(self.textEdit_14.toPlainText())
        step2 = float64(self.textEdit_15.toPlainText())

        self.sec_win = second_window(self)
        Calculation.Calculation.building(
            self, n, u0, h, x0, eps, self.sec_win, border, u10, u20, a, b, limx, lim1, lim2, step1, step2)
        self.sec_win.show()


class second_window(QtWidgets.QMainWindow, Ui_MainWindow_tab):
    def __init__(self, parent=None, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    main = Window()
    main.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        pass
