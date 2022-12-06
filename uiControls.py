from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore as core 
import sys

class MyWindow(QMainWindow):
    def __init__(self, bGround):
        super(MyWindow, self).__init__()
        self.setGeometry(10, 20, 300, 400)
        self.setFixedWidth(300)
        self.setWindowTitle("Browsie")
        self.initUI(bGround)    

        timer = core.QTimer()
        timer.timeout.connect(self.displayHistory)
        timer.start(3000)    

    def initUI(self,bGround):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Listening...")
        self.label.setStyleSheet("color: black")
        self.label.move(110,110)
        self.label.adjustSize()

        self.label6 = QtWidgets.QLabel(self)
        self.label6.setText("Listening...")
        self.label6.setStyleSheet("color: white")
        self.label6.move(110,110)
        self.label6.adjustSize()

        self.label2 = QLabel(self)
        # loading image
        self.pixmap = QPixmap('images/micWBG.png')
        self.pixmap = self.pixmap.scaled(40,70)

        # adding image to label
        self.label2.setPixmap(self.pixmap)
        self.label2.move(125,30)
        self.label2.adjustSize()
        # self.label2.mousePressEvent = self.displayUserCommand

        self.label3 = QLabel(self)
        # loading image
        self.pixmap2 = QPixmap('images/whiteBG.png')
        self.pixmap2 = self.pixmap2.scaled(35,18)

        # adding image to label
        self.label3.setPixmap(self.pixmap2)
        self.label3.move(255,15)
        self.label3.adjustSize()
        self.label3.mousePressEvent = self.darkMode 
            
        self.label4 = QLabel(self)
        # loading image
        self.pixmap3 = QPixmap('images/micDBG.png')
        self.pixmap3 = self.pixmap3.scaled(40,70)

        # adding image to label
        self.label4.setPixmap(self.pixmap3)
        self.label4.move(125,30)
        self.label4.adjustSize()
        # self.label4.mousePressEvent = self.displayUserCommand

        self.label5 = QLabel(self)
        # loading image
        self.pixmap4 = QPixmap('images/darkBG.png')
        self.pixmap4 = self.pixmap4.scaled(35,18)

        # adding image to label
        self.label5.setPixmap(self.pixmap4)
        self.label5.move(255,15)
        self.label5.adjustSize()
        self.label5.mousePressEvent = self.darkMode
        self.displayLabel1 = QLabel(self)
        self.displayLabel1.setStyleSheet("color:black;")
        self.displayLabel1.move(30,150)
        self.displayLabel2 = QLabel(self)
        self.displayLabel2.setStyleSheet("color:white;")
        self.displayLabel2.move(30,150)
        
        # All stuf for window
        if bGround == 'w':
            self.setStyleSheet("background-color: #d9d9d9;")
            self.label.setHidden(False)
            self.label2.setHidden(False)
            self.label3.setHidden(False)
            self.displayLabel1.setHidden(False)
            self.label4.setHidden(True)
            self.label5.setHidden(True)
            self.label6.setHidden(True)
            self.displayLabel2.setHidden(True)        
        else:
            self.setStyleSheet("background-color: #282424;")
            self.label = QtWidgets.QLabel(self)
            self.label.setText("Listening...")
            self.label.setStyleSheet("color: white")
            self.label.move(110,110)
            self.label.adjustSize()
            self.label.setHidden(True)
            self.label2.setHidden(True)
            self.label3.setHidden(True)
            self.displayLabel1.setHidden(True)
            self.label4.setHidden(False)
            self.label5.setHidden(False)
            self.label6.setHidden(False)
            self.displayLabel2.setHidden(False) 

        self.displayHistory()
        # self.timer = core.QTimer(self)
        # self.timer.setInterval(5000)          
        # self.timer.timeout.connect(self.displayHistory)
        
    @core.pyqtSlot()
    def update(self):
        with open('savedStates/processEnd.txt') as f:
            lines = f.readlines()
        if lines[0] == '1':
            sys.exit(self.app.exec_())

        with open('savedStates/screenMode.txt') as f:
            lines = f.readlines()
        if lines[0] == '0':
            bGround = 'w'
        else:
            bGround = 'd'
        self.initUI(bGround)



    def darkMode(self,event):
        with open('savedStates/processEnd.txt') as f:
            lines = f.readlines()
        if lines[0] == '1':
            sys.exit(self.app.exec_())

        with open('savedStates/screenMode.txt') as f:
            lines = f.readlines()
        if lines[0] == '0':
            bGround = 'w'
        else:
            bGround = 'd'
        
        myFile = open('savedStates/screenMode.txt', 'w')
        if bGround == 'w':
            myFile.write('1')
            bG = 'd'
        else:
            myFile.write('0')
            bG = 'w'
        myFile.close()
        
        self.initUI(bG)

    def displayHistory(self):
        with open('savedStates/commands.txt') as f:
            linesC = f.readlines()
        with open('savedStates/reply.txt') as f:
            linesR = f.readlines()
        
        line = ""
        index = 0
        i2 = 0
        i3 = 0
        while index < (len(linesC)+len(linesR)):
            if index%2 == 0:
                if i2 < len(linesC):
                    line+= ("User: "+linesC[i2])
                    if i2 == len(linesC) - 1:
                        line+="\n"
                    i2+=1
            else:
                if i3 < len(linesR):
                    line+= "Browsie: "
                    curr = linesR[i3]
                    n = 33 # chunk length
                    chunks = [curr[i:i+n] for i in range(0, len(curr), n)]
                    for val in chunks:
                        line+= val
                        if not val.endswith('\n'):
                            line+= '\n'
                    i3+=1
                    if i3 == len(linesR)-1:
                        line+= "\n"
            line+='------------------------------------------\n'
            index+=1
        
        self.displayLabel1.setText(line)
        self.displayLabel1.adjustSize()
        self.displayLabel2.setText(line)
        self.displayLabel2.adjustSize()
