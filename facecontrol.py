#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Facecontrol:
    """
    Modul zajišťuje sledování obličeje pomocí opencv
    """
    
    
    def __init__(self):
# default calibration_params
        self.calibration_params = 1
        pass
    def set_calibration_params(self, calibration_params):
        self.calibration_params = calibration_params

        pass

    def __calibration(self, position_precalibration):
# do some magic with self.calibration_params
        position = position_precalibration
        return position

    def get_pos(self):
        position_pc= [0 , 0 , 0]

        position = self.__calibration(position_pc)

        return position
        pass

