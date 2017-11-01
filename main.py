#　-*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PyQt5.QtOpenGL import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib as mpl
mpl.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import csv
import time as tm

time = []
x = []
y = []
z = []
twist = []
azimuth = []
elevation = []
count = 0


class GraphWidget(FigureCanvas):
    def __init__(self, parent=None):
      fig = mpl.figure.Figure()
      self.axes = fig.add_subplot(111)
      super(GraphWidget, self).__init__(fig)
      self.setMinimumSize(500, 500)
      self.x = range(0,15)
      self.y = self.x
      self.li, = self.axes.plot(self.x, self.y)
      self.axes.set_xlabel("Time[sec]")
      self.axes.set_ylabel("Altitude[m]")
      self.axes.set_ylim(0, 150)
      self.timer = QBasicTimer()
      self.timer.start(50,self)

    def timerEvent(self, e):
      self.updateFigure()

    def updateFigure(self):
      global time
      global z
      self.li.set_xdata(time[0:count])
      self.li.set_ydata(z[0:count])
      self.draw()

class QTGLWidget(QGLWidget):
  def __init__(self, parent):
    QGLWidget.__init__(self, parent)
    self.setMinimumSize(500, 500)
    
  def loadData(self):
    global count
    global time
    global twist
    global azimuth
    global elevation
    global x
    global y
    global z
    with open("./OpenGL.csv") as file:
      reader = csv.reader(file)
      # header = next(reader) #ヘッダーを飛ばす
      for row in reader:
        if(count%30 == 0):
          time.append(float(row[0]))
          twist.append(-float(row[1])-90)
          azimuth.append(float(row[2]))
          elevation.append(float(row[3]))
        count += 1
      count = 0

    with open("./Position_log.csv") as file:
      reader = csv.reader(file)
      # header = next(reader) #ヘッダーを飛ばす
      for row in reader:
        if(count%30 == 0):
          # self.time = np.append(self.time, float(row[0]))
          x.append(float(row[1]))
          y.append(float(row[2]))
          z.append(float(row[3]))
        count += 1
      count = 0

  def paintGL(self):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(10.0, 1.0, 40.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    
    glPushMatrix()
    glRotatef(float(twist[count]), 0.0, 0.0, 1.0)
    glRotatef(float(azimuth[count]), 0.0, 1.0, 0.0)
    glRotatef(float(elevation[count]), 1.0, 0.0, 0.0)
    glBegin(GL_LINES)

    #plot Codinate
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-200.0, 0.0, 0.0)
    glVertex3f(200.0, 0.0, 0.0)
    glEnd()
    glBegin(GL_LINES)
    glVertex3f(0.0, -200.0, 0.0)
    glVertex3f(0.0, 200.0, 0.0)
    glEnd()
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, -200.0)
    glVertex3f(0.0, 0.0, 200.0)
    glEnd()

    #plot Rocket
    glPushMatrix() 
    # Tube
    glPushMatrix()
    glTranslatef( 0.0, 2.0, 0.0 )
    glColor3f(1.0, 1.0, 1.0)
    self.mySolidCylinder( 0.5, 8.0, 10 )

    # Nose
    glTranslatef( 0.0, 4.0, 0.0)
    glRotatef( -90.0, 1.0, 0.0, 0.0 )
    # glColor3f(1.0, 1.0, 1.0)
    glutSolidCone( 0.5, 2.0, 10, 3 )
    glPopMatrix()
  
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)

    for i in range(4):
      glRotatef(90, 0.0, 1.0, 0.0)
      glBegin(GL_POLYGON)
      glVertex3f(0.5, -0.8, 0.0)
      glVertex3f(1.2, -1.5, 0.0)
      glVertex3f(1.2, -2.3, 0.0)
      glVertex3f(0.5, -2.0, 0.0)
      glEnd()

    glPopMatrix()
  
    glPushMatrix()
    glTranslatef(0, -2.2, 0)
    glRotatef( -90.0, 1.0, 0.0, 0.0 )
    # glColor3f(0.7, 0.7, 0.7)
    glutSolidCone(0.3, 0.5, 12, 3)
    glPopMatrix()
  
    glPopMatrix()

    # self.plotModel()
    glPopMatrix()

    self.printString()
    # if(self.count%10 == 0):print(round(self.time[self.count],1),"|",round(self.twist[self.count]),1)

    glFlush() 

  # def plotCodinate(self):
  #   glBegin(GL_LINES)
  #   glColor3f(0.0, 0.0, 1.0)
  #   glVertex3f(-200.0, 0.0, 0.0)
  #   glVertex3f(200.0, 0.0, 0.0)
  #   glEnd()
  #   glBegin(GL_LINES)
  #   glVertex3f(0.0, -200.0, 0.0)
  #   glVertex3f(0.0, 200.0, 0.0)
  #   glEnd()
  #   glBegin(GL_LINES)
  #   glVertex3f(0.0, 0.0, -200.0)
  #   glVertex3f(0.0, 0.0, 200.0)
  #   glEnd()
    

  # def plotModel(self):
    
  def printString(self):
    global count
    global time
    glColor3f(1.0,1.0,1.0)
    glRasterPos3f(4.0, -8.0, -1.0)
    string = "Time = "+str(round(time[count],1))
    string = list(string)
    for i in range(0,len(string)):
      glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(string[i]))
    
    
  def mySolidCylinder(self, r, h, n ):
    glEnable( GL_NORMALIZE )
    dq = (2*np.pi)/float(n)
    y = 0.5*h
    glPushMatrix()
    glRotatef( -dq*180.0/(2*np.pi), 0.0, 0.1, 0.0 )
    glBegin( GL_QUAD_STRIP )
    for i in range(n):
      x = r*np.cos( dq*float(i) )
      z = r*np.sin( dq*float(i) )
      glNormal3f( x,  0, z )
      glVertex3f( x,  y, z )
      glVertex3f( x, -y, z )
  
    glEnd()
    glBegin( GL_POLYGON )
    glNormal3f( 0.0, -1.0, 0.0 )
    for i in range(n):
      x = r*np.cos( dq*float(i) )
      z = r*np.sin(dq*float(i) )
      glVertex3f( x, -y, z )
  
    glEnd()
    glBegin( GL_POLYGON )
    glNormal3f( 0.0, 1.0, 0.0 )
    for i in range(n):
      x = r*np.cos( dq*float(i) )
      z = r*np.sin( dq*float(i) )
      glVertex3f( x, y, z )

    glEnd()
    glPopMatrix()
    glDisable( GL_NORMALIZE )

  def resizeGL(self, w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30.0, w/h, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
      
  def timerEvent(self, e):
    global time
    global count
    global z
    if(count == 0): self.t1 = tm.time()
    count += 5
    if(count >= len(time)-4): 
      self.t2 = tm.time()
      elapsed_time = self.t2-self.t1
      print(f"実行時間：{elapsed_time}")
      print(f"シミュレーション時間：{time[count-4]}")
      print("")
      count = 0
    self.updateGL()
    

  def initializeGL(self):
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClearDepth(1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    self.loadData() 

    self.timer = QBasicTimer()
    self.timer.start(50,self)
    

class QTWidget(QWidget):
  def __init__(self):
    QWidget.__init__(self)

    self.gl = QTGLWidget(self)
    self.graph = GraphWidget()

    hBox = QHBoxLayout()
    hBox.addWidget(self.gl)
    hBox.addWidget(self.graph)

    button_reset = QPushButton('Reset', self)
    button_reset.clicked.connect(self.timeReset)
    button_close = QPushButton('Close', self)
    button_close.clicked.connect(qApp.quit)
    button_box = QHBoxLayout()
    button_box.addWidget(button_reset)
    button_box.addWidget(button_close)

    vbox = QVBoxLayout()
    vbox.addLayout(hBox)
    vbox.addLayout(button_box)

    self.setLayout(vbox)

  
  def timeReset(self):
    global count
    count = 0

app = QApplication(sys.argv)
w = QTWidget()
w.setWindowTitle('Attitude-Plotter')
w.show()
sys.exit(app.exec_())