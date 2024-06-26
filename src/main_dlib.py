from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtCore import Qt
import sys
import cv2
import math
import numpy as np
import dlib
import imutils
from imutils import face_utils
import vlc


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Drowsiness Detector")
        self.setGeometry(100, 100, 500, 500)

        # Add a label for the video feed
        self.video_label = QLabel(self)
        self.video_label.setGeometry(50, 50, 400, 300)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setText("Video feed")

        # Add a button to start/stop the detector
        self.start_button = QPushButton(self)
        self.start_button.setGeometry(50, 400, 200, 50)
        self.start_button.setText("Start Detector")
        self.start_button.clicked.connect(self.start_detector)

        # Add a button to quit the application
        self.quit_button = QPushButton(self)
        self.quit_button.setGeometry(250, 400, 200, 50)
        self.quit_button.setText("Quit")
        self.quit_button.clicked.connect(QApplication.quit)


    def start_detector(self):
        def euclideanDist(a, b):
            return math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2))

        def ear(eye):
            return (euclideanDist(eye[1], eye[5]) + euclideanDist(eye[2], eye[4])) / (2 * euclideanDist(eye[0], eye[3]))

        alert = vlc.MediaPlayer('alarm.wav')
        frame_thresh = 30
        close_thresh = 0.25  # adjust this value to change the sensitivity of the system
        flag = 0

        print(close_thresh)

        capture = cv2.VideoCapture(0)
        avgEAR = 0
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        (leStart, leEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (reStart, reEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        while True:
            ret, frame = capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rects = detector(gray, 0)
            if len(rects):
                shape = face_utils.shape_to_np(predictor(gray, rects[0]))
                leftEye = shape[leStart:leEnd]
                rightEye = shape[reStart:reEnd]
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                leftEAR = ear(leftEye)
                rightEAR = ear(rightEye)
                avgEAR = (leftEAR + rightEAR) / 2.0
                if avgEAR < close_thresh:
                    flag += 1
                    if flag >= frame_thresh:
                        alert.play()
                elif avgEAR > close_thresh and flag:
                    alert.stop()
                    flag = 0
                cv2.drawContours(gray, [leftEyeHull], -1, (255, 255, 255), 1)
                cv2.drawContours(gray, [rightEyeHull], -1, (255, 255, 255), 1)
                writeEyes(leftEye, rightEye, frame)
            if avgEAR > close_thresh:
                alert.stop()
            cv2.imshow('Driver', gray)
            if cv2.waitKey(1) == 27:
                break

        capture.release()
        cv2.destroyAllWindows()
        alert.release()
        print("Detector stopped")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
