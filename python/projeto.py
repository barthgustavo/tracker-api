import imutils
import time
import cv2
from collections import deque
import numpy as np

tracker = cv2.TrackerKCF_create() # inicializa tracker
boundingBox = None # inicializa ROI vazia
vs = cv2.VideoCapture("../src/services/uploads/biceps.mp4") # incializa a leitura do vídeo
pts = deque(maxlen=200) # inicializa lista de pontos a serem renderizados

grayTreatment = True

while True:
    key = cv2.waitKey(1) & 0xFF # realiza a leitura de uma possível tecla
    if key == ord("s"): # se a tecla for a letra s
        boundingBox = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True) # inicia a seleção da área de interesse
        tracker.init(frame, boundingBox) # inicializa tracker

    elif key == ord("q"): # caso aperte o botão q, finaliza o while
        break

    # realiza a leitura do frame
    frame = vs.read()
    frame = frame[1]
    if frame is None:
        break

    (H, W) = frame.shape[:2]

    if boundingBox is not None: # caso já tenha sido selecionada uma área a acompanhar
        
        if grayTreatment:
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            (thresh, grayFrame) = cv2.threshold(grayFrame, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            grayFrame = cv2.cvtColor(grayFrame, cv2.COLOR_GRAY2RGB)
        
        (success, box) = tracker.update(grayFrame if grayTreatment else frame) # realiza o tracker no frame atual
        
        if success: # caso haja sucesso e o tracker tenha encontrado o que buscava
            (x, y, w, h) = [int(v) for v in box] # cria um quadrado com o que o tracker achou
            
            center = int((x + (w / 2))), int((y + (h / 2))) # acha o ponto central desta parte encontrada

            pts.appendleft(center) # adiciona à lista de pontos

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) #pode se desenhar um quadrado ao redor da área coincidente também
    
    #desenha os pontos capturados
    for i in np.arange(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue

        #cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), 5)

    cv2.imshow("Frame", frame) # renderiza frame

    time.sleep(0.1)

vs.release()
cv2.destroyAllWindows()