__author__ = 'Devesh Khosla - github.com/dekhosla'

import sys, serial, serial.tools.list_ports,warnings

from PyQt5.QtCore import QSize, QRect,QObject, pyqtSignal, QThread, pyqtSignal, pyqtSlot
import time
from PyQt5.QtWidgets import QApplication, QComboBox,QDialog, QMainWindow, QWidget, QLabel, QTextEdit, QListWidget,QListView

from PyQt5.uic import loadUi
#
import cv2
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import logging
import time
import numpy as np
import cv2
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PIL import ImageFont,ImageDraw,Image

# Define Variable

width = 511       # 1920, 720
height = 421      # 1080, 540

display_interval = 1./300.  #
window_name = 'Camera'

# synthetic data
test_img = np.random.randint(0, 255,
(height, width), 'uint8') # random image

frame = np.zeros((height,width), dtype=np.uint8)
# pre allocate
   

# Setting up logging
logging.basicConfig(level=logging.DEBUG) #options are: DEBUG, INFO, ERROR, WARNING
logger = logging.getLogger("Display")

font          = cv2.FONT_HERSHEY_SIMPLEX
textLocation0 = (10,20)
textLocation1 = (10,60)
fontScale     = 1
fontColor     = (255,255,255)
lineType      = 2

# Init Frame and Thread

measured_dps = 0.0          # displayed frames per second
num_frames = 0              # frame counter
dps_measure_time = 5.0      # count frames for 5 sec
last_time = time.perf_counter()
last_display = time.perf_counter()

# MULTI-THREADING
class Worker(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(str)
    @pyqtSlot()

    def __init__(self):
        super(Worker, self).__init__()
        self.working = True

class qt(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('qt.ui', self)
        self.thread = None
        self.worker = None
        self.pushButton.clicked.connect(self.start_loop)
        self.label_11.setText("Not detected")
        self.menuBar=self.menuBar()        


    def loop_finished(self):
        print('Loop Finished')

    def start_loop(self):
        self.portsetup()
        if self.ports:           
            self.worker = Worker()   # a new worker to perform those tasks
            self.thread = QThread()  # a new thread to run our background tasks in
            self.worker.moveToThread(self.thread)  # move the worker into the thread,do this first before connecting the signals
            self.thread.started.connect(self.worker.work) # begin our worker object's loop when the thread starts running

            self.worker.intReady.connect(self.onIntReady)
            self.pushButton_2.clicked.connect(self.stop_loop)      # stop the loop on the stop button click
            self.worker.finished.connect(self.loop_finished)       #do something in the gui when the worker loop ends

            self.worker.finished.connect(self.thread.quit)    # tell the thread it's time to stop running
            self.worker.finished.connect(self.worker.deleteLater)  #have worker mark itself for deletion
            self.thread.finished.connect(self.thread.deleteLater) # have thread mark itself for deletion

            self.thread.start()
        if not self.ports:
            self.label_11.setText("Nothing found")
 
    def portsetup(self):       
        #Port Detection START
        self.ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if 'USB' in p.description
        ]
       
        if self.ports:
            if len(self.ports) > 1:
                warnings.warn('Connected....')

            ser = serial.Serial(self.ports[0],9600)
            self.label_11.setText(self.ports[0])

#Port Detection END


    def stop_loop(self):
        self.worker.working = False

    def onIntReady(self, i):
        self.textEdit_3.append("{}".format(i))
        print(i)

    # Save the settings
    def on_pushButton_4_clicked(self):
        if self.x != 0:
            self.textEdit.setText('Settings Saved!')
        else:
            self.textEdit.setText('Please enter port and speed!')


    # TXT Save

    def on_pushButton_5_clicked(self):
        with open('Sonuc.txt', 'w') as f:
            my_text = self.textEdit_3.toPlainText()
            f.write(my_text)

    def on_pushButton_2_clicked(self):
        self.textEdit.setText('Stopped! Please click CONNECT...')

    def on_pushButton_clicked(self):
        self.completed = 0
        while self.completed < 100:
            self.completed += 0.001  
            self.progressBar.setValue(int(self.completed))
        self.textEdit.setText('Data Gathering...')

        self.label_5.setText("CONNECTED!")

        self.label_5.setStyleSheet('color: green')
        x = 1
        self.textEdit_3.setText(":")

    def on_pushButton_3_clicked(self):
        # Send data from serial port:
        mytext = self.textEdit_2.toPlainText()
        self.portsetup(self)
        print(mytext.encode())
        self.ser.write(mytext.encode())

    def on_pushButton_24_clicked(self):
        self.thread = QThread() 
        self.camera = camera()
        self.camera.start()
        self.camera.ImageUpdate.connect(self.ImageUpdateSlot)

    def ImageUpdateSlot(self, Image):
        self.label_49.setPixmap(QPixmap.fromImage(Image))




    def on_pushButton_23_clicked(self):
        measured_dps = 0.0          # displayed frames per second
        num_frames = 0              # frame counter
        dps_measure_time = 5.0      # count frames for 5 sec
        last_time = time.perf_counter()
        last_display = time.perf_counter()
        test='true'

        while (test):
            current_time = time.perf_counter()
            # update displayed frames per second

            if (current_time - last_time) >= dps_measure_time:
                measured_dps = num_frames/dps_measure_time
                logger.log(logging.DEBUG, "Status:Frames displayed per second:{}".format(measured_dps))
                last_time = current_time
                num_frames = 0

            # display frame
            if (current_time - last_display) > display_interval:
                frame = test_img.copy()
                cv2.putText(frame,"Frame:{}".format(num_frames),
            textLocation0, font, fontScale, fontColor, lineType)

                cv2.putText(frame,"Frame Rate:{}[Hz]".format(measured_dps), textLocation1, font, fontScale, fontColor,lineType)
                num_frames += 1
                last_display = current_time
                key = cv2.waitKey(1)
               
                Image1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # pil_im=Image.fromarray(Image1)
                # draw=ImageDraw.Draw(pil_im)
                # # font1=ImageFont.truetype("Roboto-Regular.ttf",50)
                # draw.text((0,0),"Frame") 
                # Image2 = cv2.cvtColor(np.array(pil_im),cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image1, 1)
                ConvertToQtFormat = QtGui.QImage(FlippedImage.data, FlippedImage.shape[1],FlippedImage.shape[0], QImage.Format_RGB888)
                # img = ConvertToQtFormat.scaled(700, 421, Qt.KeepAspectRatio) 
                self.label_49.setPixmap(QPixmap.fromImage(ConvertToQtFormat))
                if (key == 27) or (key & 0xFF== ord('q')):
                    break

#
class camera(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True
        cap = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = cap.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1],FlippedImage.shape[0], QImage.Format_RGB888)
                img = ConvertToQtFormat.scaled(511, 421, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(img)

    def stop(self):
        self.ThreadActive = False
        self.quit()
#


def run():
    app = QApplication(sys.argv)
    widget = qt()
    widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":

    run()