#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


class Facecontrol:
    """
    Modul zajišťuje sledování obličeje pomocí opencv
    """
    
    def __init__(self):
    # default calibration_params
        self.calibration_params = 1
        self.cam_source = 0       # 0 - default, 1 - external , vetsinou 0
        self.cam = cv2.VideoCapture(self.cam_source)
        self.hc = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")  # Classificator type
        self.area = None

    def get_image(self, cam):
        ret, img = cam.read()   # ret = T/F getting screen
        #fimg = np.asarray(img)  # Array for mirror image
        if ret:
            #cv2.flip(img, 1, fimg)          # Mirror image
            return img
        else:
            print "Error: No input"

    def detect(self, img):
        faces = self.hc.detectMultiScale(img, scaleFactor = 1.6, minNeighbors = 6, minSize = (100, 100), maxSize = (140, 140))  # Setting for smooth run
        return faces

    def face_center(self, faces):
        positions = []
        for face_pos in faces:
            fpos = [face_pos[0] + (face_pos[2] / 2), face_pos[1] + (face_pos[3] / 2)] # center face (nose)
            positions.append(fpos)
        return positions

    def broadcast(self):
        img = self.get_image(self.cam)
        cv2.imshow("Broadcast", img)

    def get_pos(self):
        img = self.get_image(self.cam)
        faces = self.detect(img)
        position_pc = [0, 0]

        if len(faces) > 0:
            positions = self.face_center(faces)
            position_pc = positions[0]  # X, Y prvniho obliceje

        pos = self.__calibration(position_pc) # Prepocitana kalibrace
        cv2.circle(img, (position_pc[0], position_pc[1]), 10, (0, 255, 0), 5)
        fimg = np.asarray(img)
        cv2.flip(img, 1, fimg)
        cv2.imshow("Position", fimg)
        return pos

    def set_calibration_params(self, calibration_params):
        self.area = calibration_params

    def __calibration(self, position_precalibration):
        position = position_precalibration[0]

        if self.area is None:
            return position_precalibration
        else:
            x1 = self.area['left']
            x2 = self.area['right']
            y1 = self.area['top']
            y2 = self.area['bottom']
            delka = x2 - x1

            if position >= x2:
                new_pos = (1, position_precalibration[1])
                return new_pos
            elif position <= x1:
                new_pos = (0, position_precalibration[1])
                return new_pos
            elif position > x1 and position < x2:
                pos_delka = x2 - position
                new_pos = (float(pos_delka)/delka, position_precalibration[1])
                return new_pos
