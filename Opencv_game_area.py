__author__ = 'Patrik'

import cv2
from facecontrol import Facecontrol

if __name__ == '__main__':
    fc = Facecontrol()

    while True:
        print(fc.get_pos())