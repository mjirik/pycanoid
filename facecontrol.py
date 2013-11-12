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
        self.cam_source = 1       # 0 - default, 1 - external , vetsinou 0
        self.cam = cv2.VideoCapture(self.cam_source)
        self.hc = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")  # Classificator type
        #self.okno = cv2.resizeWindow("Webcam screen", 640, 480)

    def get_image(self, cam):
        ret, img = cam.read()   # ret = T/F getting screen
        fimg = np.asarray(img)  # Array for mirror image
        if ret:
            #gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Gray image
            cv2.flip(img, 1, fimg)          # Mirror image
            return fimg
        else:
            print "Error: No input"

    def detect(self, img):
        faces = self.hc.detectMultiScale(img, scaleFactor = 1.6, minNeighbors = 6)  # Setting for smooth run
        #for face in faces:
         #   cv2.rectangle(img, (face[0], face[1]), (face[0] + face[2], face[1] + face[3]), (0, 255, 0), 1)
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

        position_pc = [0, 0]  # X,Y prvniho obliceje

        if len(faces) > 0:
            positions = self.face_center(faces)
            position_pc = positions[0]

        pos = self.__calibration(position_pc)
        cv2.circle(img, (position_pc[0], position_pc[1]), 10, (0, 255, 0), 5)
        cv2.imshow("Position", img)
        return pos

    def set_calibration_params(self, calibration_params):
        area = calibration_params
        x1 = area['left']
        x2 = area['right']
        y1 = area['top']
        y2 = area['bottom']
        l = x2 - x1





    def __calibration(self, position_precalibration):
        position = position_precalibration

        return position
