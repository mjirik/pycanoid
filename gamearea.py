__author__ = 'Patrik'

import cv2
import time
import yaml
import pickle
from facecontrol import Facecontrol


class Gamearea:
    '''
    Vymezi herni plochu. Vytvori externi soubor s herni oblasti
    '''

    def __init__(self):
        self.fc = Facecontrol()
        self.left = None
        self.right = None
        self.top = None
        self.bottom = None
        print "For LEFT border press 4, for RIGHT border press 6"

    def setsides(self, face_pos):

        if cv2.waitKey(10) == 56 and face_pos[0] != 0:      # TOP BORDER
            self.top = face_pos[1]
            print "Top side set on: "
            print self.top
            time.sleep(1)
        elif cv2.waitKey(10) == 50 and face_pos[1] != 0:    # BOTTOM BORDER
            self.bottom = face_pos[1]
            print "Bottom side set on: "
            print self.bottom
            time.sleep(1)
        elif cv2.waitKey(10) == 52 and face_pos[0] != 0:    # LEFT BORDER
            self.left = face_pos[0]
            print "Left side set on: "
            print self.left
            time.sleep(1)
        elif cv2.waitKey(10) == 54 and face_pos[1] != 0:    # RIGHT BORDER
            self.right = face_pos[0]
            print "Right side set on: "
            print self.right
            time.sleep(1)

    def check(self):
        if (self.left >= self.right) and (self.top >= self.bottom):
            return False
        else:
            return True

    def getarea(self):
        setting = True

        while setting:
            face_pos = self.fc.get_pos()    # Aktualni pozice ksichtu (x,y)
            self.setsides(face_pos)     # Vyhrazeni oblasti

            if cv2.waitKey(10) == 27:      # ESC

                if self.check():
                    print "Area created!"
                    cv2.destroyAllWindows()
                    self.saveparams(self.left, self.right, self.top, self.bottom)
                    setting = False
                    break
                else:
                    print "Error, running again"
                    cv2.destroyAllWindows()
                    self.left = None
                    self.right = None
                    self.top = None
                    self.bottom = None
                    self.getarea()

    def saveparams(self, left, right, top, bottom):
        f = open("area_params.ps", 'wb')
        dim = {'left': left, 'right': right, 'top': top, 'bottom': bottom}
        pickle.dump(dim, f)
        f.close()


if __name__ == '__main__':
    ar = Gamearea()
    ar.getarea()
    file = open('area_params.ps', 'rb')
    obj = pickle.load(file)
    print obj
