
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider
from PyQt5.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation
from fuzzy import *


class Simulation(QWidget):
    change=False
    time=0
    time_axis=[]
    y_axis=[]
    time_init=0
    frame_init=0
    graph_xmin=0
    graph_xmax=10

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Simulación con PyQt')
        self.setGeometry(100, 100, 800, 600)

        self.setup_simulation()
        self.setup_gui()
        self.init_fuzzy()
        self.show()

    def init_fuzzy(self):
        minx=-120
        maxx=120
        self.x_f = np.linspace(minx, maxx, 1000)
        self.y_f = np.linspace(0, 100, 1000)
        # 2. Definir las funciones de membresía para reglas de control
        #    en la forma "Si x es Ai, entonces y es Bi"
        A1 = [trapmf, [-120, -120, -90, -40]]
        A2 = [trimf, [-70, -40, 0]]
        A3 = [trimf, [-10, 0, 10]]
        A4 = [trimf, [0, 40, 70]]
        A5 = [trapmf, [40, 90, 120, 120]]

        B1 = [trapmf, [0, 0, 10, 20]]
        B2 = [trimf, [10, 20, 50]]
        B3 = [trimf, [30, 50, 70]]
        B4 = [trimf, [50, 80, 90]]
        B5 = [trapmf, [80, 90, 100, 100]]
        self.A = [A1, A2, A3, A4, A5]
        self.B = [B1, B2, B3, B4, B5]

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

    def setup_gui(self):
        vbox = QVBoxLayout()

        self.label = QLabel('Entrada (u): 0.0')
        vbox.addWidget(self.label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.valueChanged.connect(self.slider_value_changed)
        vbox.addWidget(self.slider)

        self.canvas = FigureCanvas(self.fig)
        vbox.addWidget(self.canvas)

        self.setLayout(vbox)

    def init_plot(self):
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(-1, 120)
        self.line.set_data([], [])
        return self.line,

    def update(self, frame):

        t = np.linspace(0, (frame-self.frame_init) / 20, frame-self.frame_init)
        response = odeint(self.plant_model, self.y0, t)
        r=0
        if(len(response)>0 ):
            r=response[-1][0]
            error=self.u-r
            print("El error es",error)
            Bp = fuzz(error, self.y_f, self.A, self.B)
            out = defuzz(self.y_f, Bp, 'centroid')
            print("salida de control es:",out)
            self.u=out
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

    def slider_value_changed(self):
        print("cambio")
        self.u = self.slider.value()
        #self.u = 1

        self.label.setText(f'Entrada (u): {self.u:.2f}')

        # Detener y reiniciar la animación con la nueva entrada
        self.ani.event_source.stop()
        self.ani.event_source.start()

        self.change=True
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sim = Simulation()
    sys.exit(app.exec_())