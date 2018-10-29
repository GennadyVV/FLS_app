import sys

# import some PyQt5 modules
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import glob
import psycopg2
import face_recognition
import cv2
import requests

# import Opencv module
import cv2

from ui_main_window import *

class MainWindow(QWidget):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        # set control_bt callback clicked  function
        self.ui.control_bt.clicked.connect(self.controlTimer)

    # view camera
    def viewCam(self):
        # read image in BGR format
        ret, frame = self.video_capture.read()
        # convert image to RGB format
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        connection = psycopg2.connect(user = "dpcwdmmygwvxqe",
                                  password = "d113638b455977377844724fea4f9e7aac7ff8dbc4685516ecbdd25d5b52a39b",
                                  host = "ec2-54-246-86-167.eu-west-1.compute.amazonaws.com",
                                  port = "5432",
                                  database = "darsad67es2t64")
        cursor = connection.cursor()
        
        rgb_small_frame = small_frame[:, :, ::-1]
        
        known_face_names_pre = glob.glob('dataset/*.jpg')
        known_image = []
        known_face_encodings = []
        known_face_names = []
        for i in range(len(known_face_names_pre)):
            image_for_append = face_recognition.load_image_file(known_face_names_pre[i])
            known_image.append(image_for_append)
            known_face_encodings.append(face_recognition.face_encodings(image_for_append)[0])
            known_face_names.append(known_face_names_pre[i][8:-4])

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        
        
        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"#; 



                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame



        if len(face_names) > 0:
            rec = face_names[0]
            #print(type(face_names[0][8:-4]))
            query = "UPDATE people SET status = 'yes' WHERE name = '" + str(rec) + "'"

            cursor.execute(query)
            connection.commit()

            #req = requests.request('GET', 'https://facevision27.herokuapp.com/refresh')

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            if name == "Unknown":
                print('Не авторизованный пользователь')
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            #cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            #cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            #font = cv2.FONT_HERSHEY_DUPLEX
            #cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)






        
        
        # get image infos
        height, width, channel = frame.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))

    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.video_capture = cv2.VideoCapture(0)
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.ui.control_bt.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.video_capture.release()
            # update control_bt text
            self.ui.control_bt.setText("Start")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())