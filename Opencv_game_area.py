__author__ = 'Patrik'

import cv2
from facecontrol import Facecontrol

if __name__ == '__main__':
    fc = Facecontrol()
    print("Create game borders")

    while True:
        face_pos = fc.get_pos()

        if cv2.waitKey(50) == 27:
            cv2.destroyAllWindows()
            break