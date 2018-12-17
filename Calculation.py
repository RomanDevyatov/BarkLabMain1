#-*- coding: utf-8 -*-
import math
#from un import *
from PyQt5 import QtWidgets
from matplotlib import rcParams
from PyQt5 import QtWidgets, QtGui, QtCore


import pylab
from matplotlib import mlab
from matplotlib.figure import Figure

import numpy as np
from un import Ui_MainWindow

from main import Window
from main import second_window 



class Calculation(Ui_MainWindow):
    def building(self, n, u, h, x, eps, secwin, borderline,  u10, u20, a, b, limx, lim1, lim2, step1, step2):
        #print(u, h, x, n)
        xlist, Ilist, L_Elist, Mark_list, hlist = [], [], [], [], []
        xlist.append(x)
        Ilist.append(u)
        hlist.append(h)

        secwin.tableWidget.setRowCount(n + 1)
        secwin.label.setText("Начальное X0 = " + str(x))
        secwin.label_2.setText("Начальное U0 = " + str(u))
        secwin.label_3.setText("Число шагов = " + str(n))
        secwin.label_3.setText("Шаг h = " + str(h))
        secwin.label_4.setText("Контроль ЛП = " + str(eps))
        secwin.label_5.setText("Выход за границу = " + str(borderline))
        secwin.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(str(x)))
        secwin.tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem(str(u)))

        cnt_inc, cnt_dec = 0, 0
        cnt_l_list, cnt_g_list = [], []
        Mark_list = []

        for i in range(n+1):
            secwin.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i)))

        def abs_solution(x, const):
            return (const*math.exp(-5*x/2))
        def sol_const(x, u):
            return (u/(math.exp(-5*x/2)))
        def loc_err(step_u, two_step_u):
            return ((two_step_u - step_u) * ((8.0) / 7.0))
        def sub_v_v2(v, v2):
            return v-v2

        def f(x, u):
            if str(self.comboBox.currentText()) == 'Test':
                return -2.5*u
            if str(self.comboBox.currentText()) == 'Main1':
                return (((math.log(x + 1)) / (x*x + 1)) * (u *u) + u - (u *u*u) * math.sin(10 * x))

        #def func(u, v):
        #    return v, -a*v*v-b*math.sin(u)

        def p1(x, u):
            return f(x, u)
        def p2(step, x, u):
            return f(x+step/2, u + step*p1(x, u) / 2)
        def p3(step, x, u):
            return f(x+step/2, u + step * p2(step, x, u)/2)
        def p4(step, x, u):
            return f(x+step, u+step*p3(step, x, u))

        def next_point_u(u, x, step):
            return (u + step * (p1(x, u) + 2 * p2(step, x, u) + 2 * p3(step, x, u) + p4(step, x, u)) / 6)
        def next_point_x(step, x):
            return x + step
        ##################################################
        def new_point(step, x, u, row_num):#сюда поступают u0 x0 - самая первая точка
            nonlocal h
            new_u = next_point_u(u, x, step)
            new_x = next_point_x(step, x)

            #считаем методом с половинным шагом
            #add_u = next_point_u(u, step / 2)
            #add_x = next_point_x(step / 2, x)

            add_u = next_point_u(next_point_u(u, x, step / 2), x, step / 2)
            add_x = next_point_x(step / 2, next_point_x(step / 2, x))

            S = loc_err(new_u, add_u)

            substr_V_V2 = sub_v_v2(new_u, add_u)
            secwin.tableWidget.setItem(row_num, 1, QtWidgets.QTableWidgetItem(str(add_x)))
            secwin.tableWidget.setItem(row_num, 2, QtWidgets.QTableWidgetItem(str(new_u)))
            secwin.tableWidget.setItem(row_num, 3, QtWidgets.QTableWidgetItem(str(add_u)))
            secwin.tableWidget.setItem(row_num, 4, QtWidgets.QTableWidgetItem(str(substr_V_V2)))
            secwin.tableWidget.setItem(row_num, 5, QtWidgets.QTableWidgetItem(str(S)))
            secwin.tableWidget.setItem(row_num, 6, QtWidgets.QTableWidgetItem(str(h)))
            nonlocal cnt_inc, cnt_dec
            if self.checkBox.isChecked():
                if abs(S) >= eps / 16 and abs(S) <= eps:
                    hlist.append(h)
                    Mark_list.append(S)
                    return new_x, new_u
                if abs(S) < eps / 16:
                    h *= 2                    
                    cnt_inc += 1
                    cnt_g_list.append(cnt_inc)
                    hlist.append(h)
                    Mark_list.append(S)
                    return new_x, new_u
                if abs(S) > eps:
                    h /= 2                    
                    cnt_dec += 1
                    cnt_l_list.append(cnt_dec)
                    return new_point(h, x, u, row_num)
            else:
                hlist.append(h)
                Mark_list.append(S)
                return new_x, new_u

        if str(self.comboBox.currentText()) == 'Test':
            ax = self.fig.add_subplot(111)
            if self.checkBox_2.isChecked():
                ax.clear()
            ax.axis([-1, 7, -1, 7])
            const = sol_const(x, u)
            exact_x = x
            exact_u = abs_solution(x, const)
            for i in range(n):
                secwin.tableWidget.setItem(i, 9, QtWidgets.QTableWidgetItem(str(exact_u)))

                prev_ex_x = exact_x
                prev_ex_u = exact_u
                L_Elist.append(abs(exact_u - u))
                x_, u_ = x, u

                xlist.append(x)
                Ilist.append(u)

                secwin.tableWidget.setItem(i, 10, QtWidgets.QTableWidgetItem(str(abs(exact_u - u))))
                secwin.tableWidget.setItem(i, 7, QtWidgets.QTableWidgetItem(str(cnt_inc)))
                secwin.tableWidget.setItem(i, 8, QtWidgets.QTableWidgetItem(str(cnt_dec)))

                x, u = new_point(h, x_, u_, i + 1)
                if x > borderline:
                    xlist.append(x)
                    break
                ax.plot([x_, x], [u_, u], '-b')
                exact_x = x
                exact_u = abs_solution(exact_x, const)
                ax.plot([prev_ex_x, exact_x], [prev_ex_u, exact_u], '-r')
            # заполняем последние строчки
            secwin.tableWidget.setItem(n, 9, QtWidgets.QTableWidgetItem(str(exact_u)))
            secwin.tableWidget.setItem(n, 10, QtWidgets.QTableWidgetItem(str(abs(exact_u - u))))
            secwin.tableWidget.setItem(n, 7, QtWidgets.QTableWidgetItem(str(cnt_inc)))
            secwin.tableWidget.setItem(n, 8, QtWidgets.QTableWidgetItem(str(cnt_dec)))

            secwin.label_10.setText("Max U = " + str(max(Ilist)))
            secwin.label_7.setText("Max X = " + str(max(xlist)))
            secwin.label_8.setText("Max h = " + str(max(hlist)))
            secwin.label_13.setText("Max Гл. Погр. = " + str(round(max(L_Elist), 9)))
            secwin.label_15.setText("Max ОЛП = " + str(max(Mark_list)))
            secwin.label_9.setText("Min h = " + str(min(hlist)))
            secwin.label_14.setText("Min Гл. Погр. = " + str(round(min(L_Elist), 9)))
            secwin.label_12.setText("Min ОЛП = " + str(min(Mark_list)))
            if self.checkBox.isChecked():
                secwin.label_11.setText("Общ кол-во увел. = " + str(max(cnt_g_list)))
                secwin.label_16.setText("Общ кол-во уменьш. = " + str(max(cnt_l_list)))
            else:
                secwin.label_11.setText("Общ кол-во увел. = --- ")
                secwin.label_16.setText("Общ кол-во уменьш. = --- ")
            secwin.tableWidget.resizeColumnsToContents()
            ax.grid(True)
            self.canvas.draw()

        if str(self.comboBox.currentText()) == 'Main1':
            ax = self.fig.add_subplot(111)
            if self.checkBox_2.isChecked():
                ax.clear()
            ax.axis([-1, 7, -1, 7])
            for i in range(n):
                x_, u_ = x, u

                xlist.append(x)
                Ilist.append(u)

                secwin.tableWidget.setItem(i, 7, QtWidgets.QTableWidgetItem(str(cnt_inc)))
                secwin.tableWidget.setItem(i, 8, QtWidgets.QTableWidgetItem(str(cnt_dec)))

                x, u = new_point(h, x_, u_, i + 1)
                if x > borderline:
                    xlist.append(x)
                    break
                ax.plot([x_, x], [u_, u], '-b')
            secwin.tableWidget.setItem(n, 7, QtWidgets.QTableWidgetItem(str(cnt_inc)))
            secwin.tableWidget.setItem(n, 8, QtWidgets.QTableWidgetItem(str(cnt_dec)))

            secwin.label_10.setText("Max U = " + str(max(Ilist)))
            secwin.label_7.setText("Max X = " + str(max(xlist)))
            secwin.label_8.setText("Max h = " + str(max(hlist)))
            secwin.label_15.setText("Max ОЛП = " + str(max(Mark_list)))
            secwin.label_9.setText("Min h = " + str(min(hlist)))
            secwin.label_14.setText("Min Гл. Погр. = " + "---")
            secwin.label_13.setText("Max Гл. Погр. = " + "---")
            secwin.label_12.setText("Min ОЛП = " + str(min(Mark_list)))
            if self.checkBox.isChecked():
                secwin.label_11.setText("Общ кол-во увел. = " + str(cnt_inc))
                secwin.label_16.setText("Общ кол-во уменьш. = " + str(cnt_dec))
            else:
                secwin.label_11.setText("Общ кол-во увел. = --- ")
                secwin.label_16.setText("Общ кол-во уменьш. = --- ")
            secwin.label_17.setText("")
            secwin.label_18.setText("")
            secwin.tableWidget.resizeColumnsToContents()
            ax.grid(True)
            self.canvas.draw()

        if str(self.comboBox.currentText()) == 'Main2':
            cnt_dec, cnt_inc = 0, 0
            s1, s2 = 0, 0
            h_list = []
            S1list, S2list = [], []
            S1list.append(s1)
            S2list.append(s2)
            secwin.tableWidget.setItem(0, 6, QtWidgets.QTableWidgetItem(str(h)))
            secwin.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(str(x)))
            #secwin.tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem(str(u10)))
            #secwin.tableWidget.setItem(0, 3, QtWidgets.QTableWidgetItem(str(u20)))

            def du1(v1, v2):
                return v2

            def du2(v1, v2):
                return (- a*(v2*v2) - (b*math.sin(v1)))

            def calc_coef_for_system(u1, u2, step):
                q = [[0] * 2] * 5
                res = np.array(q, dtype=np.float)
                res[0][0] = du1(u1, u2)
                res[0][1] = du2(u1, u2)

                res[1][0] = du1(u1 + step * res[0][0] / 2, u2 + step * res[0][0] / 2)
                res[1][1] = du2(u1 + step * res[0][1] / 2, u2 + step * res[0][1] / 2)

                res[2][0] = du1(u1 + step * (res[0][0] + res[1][0]) / 6, u2 + step * (res[0][0] + res[1][0]) / 6)
                res[2][1] = du2(u1 + step * (res[0][1] + res[1][1]) / 6, u2 + step * (res[0][1] + res[1][1]) / 6)

                res[3][0] = du1(u1 + step * (res[0][0] + 3 * res[2][0]) / 8,
                                u2 + step * (res[0][0] + 3 * res[2][0]) / 8)
                res[3][1] = du2(u1 + step * (res[0][1] + 3 * res[2][1]) / 8,
                                u2 + step * (res[0][1] + 3 * res[2][1]) / 8)

                res[4][0] = du1(u1 + step * (res[0][0] - 3 * res[2][0] + 4 * res[3][0]) / 2,
                                u2 + step * (res[0][0] - 3 * res[2][0] + 4 * res[3][0]) / 2)
                res[4][1] = du2(u1 + step * (res[0][1] - 3 * res[2][1] + 4 * res[3][1]) / 2,
                                u2 + step * (res[0][1] - 3 * res[2][1] + 4 * res[3][1]) / 2)
                return res

            def calc_coef_for_system_ps(du1, du2, u1, u2, step):
                q = [[0] * 2] * 4
                res = np.array(q, dtype=np.float64)
                res[0][0] = du1(u1, u2)
                res[0][1] = du2(u1, u2)

                res[1][0] = du1(u1 + step * res[0][0] / 2, u2 + step * res[0][0] / 2)
                res[1][1] = du2(u1 + step * res[0][1] / 2, u2 + step * res[0][1] / 2)

                res[2][0] = du1(u1 + step * res[1][0] / 2, u2 + step * res[1][0] / 2)
                res[2][1] = du2(u1 + step * res[1][1] / 2, u2 + step * res[1][1] / 2)

                res[3][0] = du1(u1 + step * res[2][0], u2 + step * res[2][0])
                res[3][1] = du2(u1 + step * res[2][1], u2 + step * res[2][1])

                return res

            def next_point(x, u1, u2, number_r):
                nonlocal h
                x_new = x + h
                h_list.append(h)
                K = calc_coef_for_system(u1, u2, h)
                s1 = h * (2 * K[0][0] - 9 * K[2][0] + 8 * K[3][0] - K[4][0]) / 30
                s2 = h * (2 * K[0][1] - 9 * K[2][1] + 8 * K[3][1] - K[4][1]) / 30
                secwin.tableWidget.setItem(number_r, 2, QtWidgets.QTableWidgetItem(str(abs(s1))))
                secwin.tableWidget.setItem(number_r, 3, QtWidgets.QTableWidgetItem(str(abs(s2))))
                u1_new = u1 + h * (K[0][0] + 4 * K[3][0] + K[4][0]) / 6
                u2_new = u2 + h * (K[0][1] + 4 * K[3][1] + K[4][1]) / 6
                secwin.tableWidget.setItem(number_r, 1, QtWidgets.QTableWidgetItem(str(x_new)))
                #secwin.tableWidget.setItem(number_r, 0, QtWidgets.QTableWidgetItem(str(number_r)))
                #secwin.tableWidget.setItem(number_r, 2, QtWidgets.QTableWidgetItem(str(u1_new)))
                #secwin.tableWidget.setItem(number_r, 3, QtWidgets.QTableWidgetItem(str(u2_new)))
                nonlocal cnt_dec, cnt_inc
                if self.checkBox.isChecked():
                    if abs(s1) >= eps / 16 and abs(s2) >= eps / 16 and abs(s1) <= eps and abs(s2) <= eps:
                        S1list.append(abs(s1))
                        S2list.append(abs(s2))
                        return x_new, u1_new, u2_new
                    elif abs(s1) > eps or abs(s2) > eps:
                        cnt_dec += 1
                        h /= 2
                        return next_point(x, u1, u2, number_r)
                    elif abs(s1) < eps / 16 and abs(s2) < eps / 16:
                        cnt_inc += 1
                        h *= 2
                        S1list.append(abs(s1))
                        S2list.append(abs(s2))
                        return x_new, u1_new, u2_new
                    else:
                        S1list.append(abs(s1))
                        S2list.append(abs(s2))
                        return x_new, u1_new, u2_new
                else:
                    return x_new, u1_new, u2_new

            def new_point_for_PS(x, u1, u2):
                nonlocal h
                x_new = x + h
                K = calc_coef_for_system_ps(du1, du2, u1, u2, h)
                u1_new = u1 + h * (K[0][0] + 2 * K[1][0] + 2 * K[2][0] + K[3][0]) / 6
                u2_new = u2 + h * (K[0][1] + 2 * K[1][1] + 2 * K[2][1] + K[3][1]) / 6
                K = calc_coef_for_system_ps(du1, du2, u1, u2, h / 2)
                u1_half = u1 + h * (K[0][0] + 2 * K[1][0] + 2 * K[2][0] + K[3][0]) / 12
                u2_half = u2 + h * (K[0][1] + 2 * K[1][1] + 2 * K[2][1] + K[3][1]) / 12
                K = calc_coef_for_system_ps(du1, du2, u1_half, u2_half, h / 2)
                u1_half = u1_half + h * (K[0][0] + 2 * K[1][0] + 2 * K[2][0] + K[3][0]) / 12
                u2_half = u2_half + h * (K[0][1] + 2 * K[1][1] + 2 * K[2][1] + K[3][1]) / 12
                s1 = (u1_new - u1_half) * 16.0 / 15.0
                s2 = (u2_new - u2_half) * 16.0 / 15.0

                if self.checkBox.isChecked():
                    if abs(s1) <= eps and abs(s2) <= eps and abs(s1) >= eps / 16 and abs(s2) >= eps / 16:
                        return x_new, u1_new, u2_new
                    elif abs(s1) > eps or abs(s2) > eps:
                        h /= 2
                        return new_point_for_PS(x, u1, u2)
                    elif abs(s1) < eps / 16 and abs(s2) < eps / 16:
                        h *= 2
                        return x_new, u1_new, u2_new
                    else:
                        return x_new, u1_new, u2_new
                else:
                    return x_new, u1_new, u2_new

            def phase_plane(u10, u20, x0):
                beg_point_u1 = np.arange(u10 - lim1, u10 + lim1, step1, dtype=np.float64)
                beg_point_u2 = np.arange(u20 - lim2, u20 + lim2, step2, dtype=np.float64)
                x_PS = x0
                for i in beg_point_u2:
                    for j in beg_point_u1:
                        u1list_PS = []
                        xlist_PS, u2list_PS = [], []
                        xlist_PS.append(x_PS)
                        u2list_PS.append(i)
                        u1list_PS.append(j)
                        u, p = j, i
                        while abs(u) < lim1 and abs(p) < lim2 and x_PS < limx:
                            x_PS, u, p = new_point_for_PS(x_PS, u, p)
                            xlist_PS.append(x_PS)
                            u1list_PS.append(u)
                            u2list_PS.append(p)
                        ax3.plot(u2list_PS, u1list_PS, '-y')
                        x_PS = x0

            ax1= self.fig.add_subplot(221)
            ax2 = self.fig.add_subplot(223)
            ax3 = self.fig.add_subplot(122)

            if self.checkBox_2.isChecked():
                ax1.clear()
                ax2.clear()
                ax3.clear()
            #ax1.axis([-1, 15, -1, 10])
            #ax2.axis([-1, 15, -1, 10])
            u, p = u10, u20
            x_ = x
            i = 0
            xlist, u1list, u2list = [], [], []
            u1list.append(u10)
            u2list.append(u20)
            xlist.append(x)
            while x_ < borderline and abs(u) < 200 and abs(p) < 200:
                x_, u, p = next_point(x_, u, p, i + 1)
                secwin.tableWidget.setItem(i + 1, 6, QtWidgets.QTableWidgetItem(str(h)))
                secwin.tableWidget.setItem(i + 1, 7, QtWidgets.QTableWidgetItem(str(cnt_dec)))
                secwin.tableWidget.setItem(i + 1, 8, QtWidgets.QTableWidgetItem(str(cnt_inc)))
                xlist.append(x_)
                u1list.append(u)
                u2list.append(p)
                i += 1
                #if i>n: break
            #if self.checkBox.isChecked():
            line1, =ax1.plot(xlist, u1list, '-g', label='С контролем ЛП')
            line2, = ax2.plot(xlist, u2list, '-m', label='С контролем ЛП')
            #if self.checkBox.isChecked():
            secwin.label_15.setText("Максимальная оценка ЛП 1 = " + str(round(max(S1list), 9)))
            secwin.label_17.setText("Максимальная оценка ЛП 2 = " + str(round(max(S2list), 9)))
            secwin.label_18.setText("Минимальная оценка ЛП 2 = " + str(round(min(S2list), 9)))
            secwin.label_8.setText("Max h = " + str(max(h_list)))
            secwin.label_9.setText("Min h = " + str(min(h_list)))
            secwin.label_10.setText("Max U = " + "----")
            secwin.label_7.setText("Max X = " + "----")
            secwin.label_14.setText("Min Гл. Погр. = " + "---")
            secwin.label_13.setText("Max Гл. Погр. = " + "---")
            secwin.label_12.setText("Минимальная оценка ЛП 1 = " + str(round(min(S1list), 9)))

            if self.checkBox.isChecked():
                secwin.label_11.setText("Общ кол-во увел. = " + str(cnt_inc))
                secwin.label_16.setText("Общ кол-во уменьш. = " + str(cnt_dec))
            else:
                secwin.label_11.setText("Общ кол-во увел. = --- ")
                secwin.label_16.setText("Общ кол-во уменьш. = --- ")

            secwin.tableWidget.resizeColumnsToContents()

            phase_plane(u10, u20, x)
     
            ax1.grid(True)
            ax2.grid(True)
            ax3.grid(True)
            self.canvas.draw()




