import cv2 as cv
import numpy as np

cam = cv.VideoCapture(0)

cam.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)


if not (cam.isOpened()):
    print("Error de conexion")

while(1):
    frame = cam.read()
    cv.imshow('Prueba', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv.destroyAllWindows()