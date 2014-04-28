# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 21:15:11 2014

@author: patrik
"""
import yaml

f = file('kinect_borders.config','rb')
obj = yaml.load(f)
f.close()
print obj['bottom']
