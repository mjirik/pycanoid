#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2

class Facecontrol:
    """
    Modul zajišťuje sledování obličeje pomocí opencv
    """
    
    def __init__(self):
# default calibration_params
        self.calibration_params = 1
        self.cam_source = 1      # 0 - default, 1 - external
        self.cam = cv2.VideoCapture(self.cam_source)
        self.hc = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
        #self.okno = cv2.resizeWindow("Webcam screen", 640, 480)

    def get_image(self, cam):
        ret, img = cam.read()
        if ret:
            gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            return gimg
        else:
            print "Error: No input"

    def detect(self, img):
        faces = self.hc.detectMultiScale(img)
        for face in faces:
            cv2.rectangle(img, (face[0], face[1]), (face[0] + face[2], face[1] + face[3]), (255, 0, 0), 3)
        return faces

    def face_center(self, faces):
        positions = []
        for face_pos in faces:
            fpos = [face_pos[0] + (face_pos[2] / 2), face_pos[1] + (face_pos[3] / 2)]
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
            position_pc = positions[0]

        pos = self.__calibration(position_pc)
        cv2.imshow("Position", img)
        return pos

    def set_calibration_params(self, calibration_params):
        self.calibration_params = calibration_params
        pass

    def __calibration(self, position_precalibration):
# do some magic with self.calibration_params
        position = position_precalibration
        return position
