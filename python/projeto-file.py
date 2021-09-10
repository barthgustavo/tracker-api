#fazer pegar pelo tempo informado
#fazer pegar o tamanho dinamico do quadro

import argparse
import cv2
from collections import deque
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, help="path to input video file")
args = vars(ap.parse_args())

args["video"] = "../src/services/uploads/biceps.mp4"

if args["video"] is None:
    print("path to video was not supplied")
    exit()


tracker = cv2.TrackerKCF_create() # inicializa tracker
boundingBox = (311, 261, 100, 100)

cap = cv2.VideoCapture(args["video"])
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
#get dimensions from video
out = cv2.VideoWriter('output.mp4', fourcc, 29.97, (640,360))
pts = deque(maxlen=200)
startedTracking = False

while(cap.isOpened()):
    ret, frame = cap.read()
    

    if ret == True:
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

        out.write(frame)
    else:
        break

cap.release()