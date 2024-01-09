from PyQt5 import QtWidgets, uic, QtGui,QtCore
import sys
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation
from fuzzy import *
import imagen_rc
from matplotlib.figure import Figure

class Ui(QtWidgets.QMainWindow):
    change=False
    time=0
    time_axis=[]
    y_axis=[]
    time_init=0
    frame_init=0
    graph_xmin=0
    graph_xmax=10

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)
        self.setpoint=20
        self.init_fuzzy()
        self.setup_simulation()
        self.setup_gui()           
        
        self.show()
        self.initSignals()
        self.le_setpoint.setText(str(self.setpoint))

    def initSignals(self):
        self.btn_setpoint.clicked.connect(self.changeSetpoint)
    
    def changeSetpoint(self):
        self.setpoint=round(float(self.le_setpoint.text()),2)
    
    def setup_gui(self):
        layout = QtWidgets.QVBoxLayout(self.widget)
        layout2 = QtWidgets.QVBoxLayout(self.widget_2)
        layout3 = QtWidgets.QVBoxLayout(self.widget_3)

        self.figura = Figure()

        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        # Universo de discurso para el error
        e = np.linspace(-120, 120, 1000)

        # Funciones de pertenencia para el error
        ENG = trapmf(e, self.va1)
        ENP = trimf(e, self.va2)
        EC = trimf(e, self.va3)
        EPP = trimf(e, self.va4)
        EPG = trapmf(e, self.va5)

        #gráficos para el error
        self.fig2, self.ax2 = plt.subplots()
        self.canvas2 = FigureCanvas(self.fig2)
        self.ax2.plot(e, ENG, label="ENG")
        self.ax2.plot(e, ENP, label="ENP")
        self.ax2.plot(e, EC, label="EC")
        self.ax2.plot(e, EPP, label="EPP")
        self.ax2.plot(e, EPG, label="EPG")
        self.canvas2.draw()
        layout2.addWidget(self.canvas2)

        # Universo de discurso para el termostato (voltaje del motor)
        p = np.linspace(0, 100, 1000)

        # Funciones de pertenencia para el error
        PBG = trapmf(p, self.vb1)
        PBM = trimf(p, self.vb2)
        PC = trimf(p, self.vb3)
        VPP = trimf(p, self.vb4)
        VPG = trapmf(p, self.vb5)

        #gráficos para el error
        self.fig3, self.ax3 = plt.subplots()
        self.canvas3 = FigureCanvas(self.fig3)
        self.ax3.plot(p, PBG, label="PBG")
        self.ax3.plot(p, PBM, label="PBM")
        self.ax3.plot(p, PC, label="PC")
        self.ax3.plot(p, VPP, label="VPP")
        self.ax3.plot(p, VPG, label="VPG")
        self.canvas3.draw()
        layout3.addWidget(self.canvas3)

    def setup_simulation(self):
        self.t_ini=0
        self.numerator = [1.2]
        self.denominator = [300, 1]
        self.tau = 1.0  # constante de tiempo
        self.y0 = 0.0
        self.u = 1  # Variable de entrada
        

        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], label='Salida')
        self.ax.legend()

        self.interval_ms = 100
        self.ani = FuncAnimation(self.fig, self.update, init_func=self.init_plot, blit=True,
                                 interval=self.interval_ms)
        
    def init_fuzzy(self):
        minx=-120
        maxx=120
        self.x_f = np.linspace(minx, maxx, 1000)
        self.y_f = np.linspace(0, 100, 1000)

        self.va1=[-120, -120, -90, -40]
        self.va2=[-70, -40, 0]
        self.va3=[-40, 0, 40]
        self.va4=[0, 40, 70]
        self.va5=[40, 90, 120, 120]

        A1 = [trapmf, self.va1]
        A2 = [trimf, self.va2]
        A3 = [trimf, self.va3]
        A4 = [trimf, self.va4]
        A5 = [trapmf, self.va5]

        #self.vb1=[0, 0, 10, 20]
        #self.vb2=[10, 30, 50]
        #self.vb3=[30, 50, 70]
        #self.vb4=[50, 80, 90]
        #self.vb5=[80, 90, 100, 100]

        self.vb1=[0, 0, 2, 5]
        self.vb2=[0, 5, 15]
        self.vb3=[10, 15, 20]
        self.vb4=[15, 25, 40]
        self.vb5=[30, 50, 100, 100]

        B1 = [trapmf, self.vb1]
        B2 = [trimf, self.vb2]
        B3 = [trimf, self.vb3]
        B4 = [trimf, self.vb4]
        B5 = [trapmf, self.vb5]
        self.A = [A1, A2, A3, A4, A5]
        self.B = [B1, B2, B3, B4, B5]

    def init_plot(self):
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(-1, 50)
        self.line.set_data([], [])
        return self.line,

    def update(self, frame):
        t = np.linspace(0, (frame-self.frame_init) / 20, frame-self.frame_init)
        response = odeint(self.plant_model, self.y0, t)
        r=0
        if(len(response)>0 ):
            r=response[-1][0]
            error=self.setpoint-r
            self.le_error.setText(str(round(error,2)))
            #print("El error es",error)
            Bp = fuzz(error, self.y_f, self.A, self.B)
            out = defuzz(self.y_f, Bp, 'centroid')
            #print("salida de control es:",out)
            self.u=out
            self.le_tempReal.setText(str(round(r,2))+" C")
            self.le_tempReal_2.setText(str(round(r,2))+" C")
            self.le_outControl.setText(str(round(self.u,2))+" %")
            #print(response)
            #print(response[-1][0])
            #response = np.hstack((self.time_axis,response[0]))
            self.y0=response[-1][0]
            if self.change:
                print("cambio")
                self.y0=response[-1][0]
                print(self.y0)
                self.time_init=frame/10
                self.frame_init=frame
                self.change=False
        if (self.time>self.graph_xmax):
            self.graph_xmin=self.graph_xmin+10
            self.graph_xmax=self.graph_xmax+10
            self.ax.set_xlim(self.graph_xmin, self.graph_xmax)
        
        self.time=self.time+0.1
        self.time_axis.append(self.time)
        self.y_axis.append(r)
        self.line.set_data(self.time_axis,self.y_axis)
        #self.line.set_data(t, response)
        return self.line,

    def plant_model(self, y, t):
        #dydt = (self.u - y) / self.tau
        dydt = (self.numerator[0] * self.u - self.denominator[1] * y) / self.denominator[0]
        return dydt