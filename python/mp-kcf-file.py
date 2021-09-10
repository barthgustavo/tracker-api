#fazer pegar pelo tempo informado
#fazer pegar o tamanho dinamico do quadro

import argparse
import cv2
from collections import deque
import numpy as np
import mediapipe as mp
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, help="path to input video file")
ap.add_argument("-t", "--time", type=str, help="time to start the processing")
args = vars(ap.parse_args())

if args["video"] is None:
    print("path to video was not supplied")
    exit()

if args["time"] is None:
    args["time"] = 0

tracker = cv2.TrackerKCF_create() # inicializa tracker
boundingBox = (360, 48, 100, 100)

filename = os.path.join(fileDir, "../uploads/" + args["video"])
filename = os.path.abspath(os.path.realpath(filename))

cap = cv2.VideoCapture(filename)
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
#get dimensions from video

processedFilename = os.path.join(fileDir, "../uploads/processed-" + args["video"])
processedFilename = os.path.abspath(os.path.realpath(processedFilename))

out = cv2.VideoWriter(processedFilename, fourcc, 29.97, (640,360))
pts = deque(maxlen=200)
startedTracking = False

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while(cap.isOpened()):
        ret, frame = cap.read()        

        if ret == True:
            if not np.greater_equal(cap.get(cv2.CAP_PROP_POS_MSEC), float(args["time"]) * 1000):
                continue

            if(startedTracking is False):
                startedTracking = True
                tracker.init(frame, boundingBox)
            
            (success, box) = tracker.update(frame)
            if success:
                (x, y, w, h) = [int(v) for v in box] # cria um quadrado com o que o tracker achou
                center = int((x + (w / 2))), int((y + (h / 2))) # acha o ponto central desta parte encontrada
                pts.appendleft(center)

            for i in np.arange(1, len(pts)):
                if pts[i - 1] is None or pts[i] is None:
                    continue

                cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), 5)
            
            #mediapipe
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            frame.flags.writeable = False
            results = pose.process(frame)

            # Draw the pose annotation on the image.
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            out.write(frame)
        else:
            break

cap.release()