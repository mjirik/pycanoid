author = "Pat"

import cv2
import numpy

cam_source = 1      # 0 - default, 1 - external
cam = cv2.VideoCapture(cam_source)
hc = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
cv2.resizeWindow("Webcam screen", 640, 480)


def get_image(cam):
    ret, img = cam.read()
    if ret:
        gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gimg
    else:
        print "Error: No input"


def detect(img):
    faces = hc.detectMultiScale(img)
    for face in faces:
        cv2.rectangle(img, (face[0], face[1]), (face[0] + face[2], face[1] + face[3]), (255, 0, 0), 3)
    return faces


def face_center(faces):
    positions = []

    for face_pos in faces:
        fpos = [face_pos[0] + (face_pos[2] / 2), face_pos[1] + (face_pos[3] / 2)]
        positions.append(fpos)
    return positions

if __name__ == "__main__":

    while True:
        img = get_image(cam)
        faces = detect(img)

        if len(faces) > 0:
            pos = face_center(faces)
            print 'Faces:', len(faces)
            print 'Positions: ', pos
            print
        else:
            print("No face detected")
            print

        cv2.imshow("Webcam screen", img)

        if cv2.waitKey(10) == 27:
            cv2.destroyAllWindows()
            break