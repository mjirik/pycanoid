__author__ = 'Patrik'

import cv2
from facecontrol import Facecontrol


class Gamearea:
    '''
    Vymezi herni plochu. Vraci max levou a pravou stranu
    '''

    def __init__(self):
        self.fc = Facecontrol()
        self.left = None
        self.right = None
        self.area = (self.left, self.right)
        print "For LEFT border press 4, for RIGHT border press 6"

    def setsides(self, face_pos):

        if cv2.waitKey(10) == 52 and face_pos[0] != 0:
            self.left = face_pos[0]
            print "Left side set on: "
            print self.left

        if cv2.waitKey(10) == 54 and face_pos[1] != 0:
            self.right = face_pos[0]
            print "Right side set on: "
            print self.right

    def check(self, left, right):
        if left > right:
            return False
        else:
            return True

    def getarea(self):
        setting = True

        while setting:
            face_pos = self.fc.get_pos()
            self.setsides(face_pos)

            if cv2.waitKey(10) == 27:

                if self.check(self.left, self.right):
                    print "Area created!"
                    cv2.destroyAllWindows()
                    setting = False
                else:
                    print "Error, running again"
                    cv2.destroyAllWindows()
                    self.left = None
                    self.right = None
                    self.getarea()

        return self.left, self.right

if __name__ == '__main__':
    ar = Gamearea()
    area = ar.getarea()
    print area
