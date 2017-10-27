################################################
#                Classes by                    #
#              By Geoff Samuel                 #
#            www.GeoffSamuel.com               #
#            Info@GeoffSamuel.com              #
################################################

# Import Modules
from PyQt4 import QtGui,QtCore, uic
import os.path, sys
import tensorflow as tf
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir) + '/Neural Network/')
from load_neural_network import *
from plotting import *
from scipy import ndimage, convolve, misc
from numpy import nanmean
import numpy as np

# Load the UI File
gui_model = 'GUI.ui'
form, base = uic.loadUiType(gui_model)
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir) + '/Images/'

# Downsampel Resolution
def downsample(myarr,factor,estimator=nanmean):
    ys,xs = myarr.shape
    crarr = myarr[:ys-(ys % int(factor)),:xs-(xs % int(factor))]
    dsarr = estimator( np.concatenate([[crarr[i::factor,j::factor]
        for i in range(factor)] 
        for j in range(factor)]), axis=0) 
    return dsarr

# Point class for shapes      
class Point:
    x, y = 0, 0
    def __init__(self, nx=0, ny=0): 
        self.x = nx
        self.y = ny
        
# Single shape class
class Shape:
    location = Point()
    number = 0
    def __init__(self, L, S):
        self.location = L
        self.number = S

# Cotainer Class for all shapes
class Shapes:
    shapes = []
    def __init__(self):
        self.shapes = []
    # Returns the number of shapes
    def NumberOfShapes(self):
        return len(self.shapes)
    # Add a shape to the database, recording its position
    def NewShape(self,L,S):
        shape = Shape(L,S)
        self.shapes.append(shape)
    # Returns a shape of the requested data.
    def GetShape(self, Index):
        return self.shapes[Index]
    #Removes any point data within a certain threshold of a point.
    def RemoveShape(self, L, threshold):
        i = 0
        while True:
            if(i==len(self.shapes)):
                break 
            #Finds if a point is within a certain distance of the point to remove.
            if((abs(L.x - self.shapes[i].location.x) < threshold) and (abs(L.y - self.shapes[i].location.y) < threshold)):
                #removes all data for that number
                del self.shapes[i]
                for n in range(len(self.shapes)-i):
                    self.shapes[n+i].number+= 1
                i -= 1
            i += 1

class Painter(QtGui.QWidget):
    ParentLink = 0
    MouseLoc = Point(0,0)  
    LastPos = Point(0,0)  

    def __init__(self,parent):
        super(Painter, self).__init__()
        self.ParentLink = parent
        self.MouseLoc = Point(0,0)
        self.LastPos = Point(0,0) 
    #Mouse down event
    def mousePressEvent(self, event): 
        self.ParentLink.IsPainting = True
        self.ParentLink.ShapeNum += 1
        self.LastPos = Point(0,0)    
    #Mouse Move event        
    def mouseMoveEvent(self, event):
        if(self.ParentLink.IsPainting == True):
            self.MouseLoc = Point(event.x(),event.y())
            if((self.LastPos.x != self.MouseLoc.x) and (self.LastPos.y != self.MouseLoc.y)):
                self.LastPos =  Point(event.x(),event.y())
                self.ParentLink.DrawingShapes.NewShape(self.LastPos, self.ParentLink.ShapeNum)
            self.repaint()             
    #Mose Up Event         
    def mouseReleaseEvent(self, event):
        if(self.ParentLink.IsPainting == True):
            self.ParentLink.IsPainting = False
    # Paint Event
    def paintEvent(self,event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.drawLines(event, painter)
        painter.end()
    # Draw the line       
    def drawLines(self, event, painter):
        painter.setRenderHint(QtGui.QPainter.Antialiasing);
        
        for i in range(self.ParentLink.DrawingShapes.NumberOfShapes()-1):     
            T = self.ParentLink.DrawingShapes.GetShape(i)
            T1 = self.ParentLink.DrawingShapes.GetShape(i+1) 
            if(T.number== T1.number):
                pen = QtGui.QPen(QtGui.QColor(0, 0, 0), 10, QtCore.Qt.SolidLine)
                painter.setPen(pen)
                painter.drawLine(T.location.x,T.location.y,T1.location.x,T1.location.y)
        
#Main UI Class
class CreateUI(base, form):
    DrawingShapes = Shapes()
    PaintPanel = 0
    IsPainting = False
    ShapeNum = 0

    def __init__(self):
        super(base,self).__init__()
        self.setupUi(self)
        self.setObjectName('Rig Helper')
        self.PaintPanel = Painter(self)
        self.PaintPanel.close()
        self.DrawingFrame.insertWidget(0,self.PaintPanel)
        self.DrawingFrame.setCurrentWidget(self.PaintPanel)

        self.label = QtGui.QLabel(self)
        self.label.setGeometry(QtCore.QRect(460, 70, 280, 280))
        self.pixmap = QtGui.QPixmap(image_path + str(-1) +".png")
        self.label.setPixmap(self.pixmap)

        QtCore.QObject.connect(self.Clear_Button, QtCore.SIGNAL("clicked()"),self.ClearSlate)
        QtCore.QObject.connect(self.Predict_Button, QtCore.SIGNAL("clicked()"),self.PredictNumber)
    # Reset Button
    def ClearSlate(self):
        self.DrawingShapes = Shapes()
        self.PaintPanel.repaint()  
        self.pixmap = QtGui.QPixmap(image_path + str(-1) +".png")
        self.label.setPixmap(self.pixmap)
    # Predict Button
    def PredictNumber(self): 
        arr = np.full((280, 280), 0).astype(np.float32)               
        for shape in self.DrawingShapes.shapes:
            arr[shape.location.y, shape.location.x] = 255
        arr = downsample(arr, 10)
        pred = nn_test(X_b = X_b, arr=arr)
        print(image_path + str(pred) +".png")
        self.pixmap = QtGui.QPixmap(image_path + str(int(pred)) +".png")
        self.label.setPixmap(self.pixmap)
        display_digit(arr)
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main_window = CreateUI()
    main_window.show()
    sys.exit(app.exec_())