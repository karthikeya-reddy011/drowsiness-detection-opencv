# Driver Drowsiness Detection System

This repository contains code for a driver drowsiness detection system. The system uses OpenCV to detect eye closure and head pose. If the driver's eyes are closed for a certain period of time, or if their head is tilted too far forward, the system will sound an alarm to warn the driver.

## Features

* Detects eye closure and head pose
* Sounds an alarm if the driver is drowsy
* Can be used with a webcam or a video file

## Requirements

* Python 3.6 or higher
* OpenCV 3.4 or higher

## Installation

1. Install the dependencies:

pip install -r requirements.txt


2. Run the system:

python driver_drowsiness_detection.py


## Usage

The system will then detect eye closure and head pose in the webcam feed. If the driver's eyes are closed for a certain period of time, or if their head is tilted too far forward, the system will sound an alarm to warn the driver.

## Troubleshooting

If you have any problems, please open an issue on the GitHub repository.

## Contributing

If you would like to contribute to the project, please fork the repository and submit a pull request.


** Note: Please download shape_predictor_68_face_landmarks.dat and add it in the Datasets repository, You can download using this link: https://www.kaggle.com/datasets/sergiovirahonda/shape-predictor-68-face-landmarksdat/download?datasetVersionNumber=1 **
