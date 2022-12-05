from PyQt5.QtWidgets import *
from uiControls import *
from assistantControl import *
from multiprocessing import Process
import sys

def window():
    with open('images/savedState.txt') as f:
        lines = f.readlines()
    if lines[0] == '0':
        bGround = 'w'
    else:
        bGround = 'd' 
    
    myFile = open('history/closure.txt', 'w')
    myFile.write('0')
    myFile.close()
   
    app = QApplication(sys.argv)
    win = MyWindow(bGround)
    win.show()

    sys.exit(app.exec_())
    

if __name__ == '__main__':
     # creating thread
    # window()
    thread = []
    thread.append(Process(target=window))
    # thread.append(Process(target=assistantController))
    for x in thread:
        x.start()
